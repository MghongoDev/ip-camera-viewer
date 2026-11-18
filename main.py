"""Run the viewer loop and keep every exit path safe.

Phases 2 to 5 of the implementation guide; TC01, TC02, TC03, TC06, TC07,
TC08, TC09 and TC10. See ADR-0002, ADR-0003, ADR-0004 and ADR-0005.
"""

import logging
import os
import sys
import time

import cv2

import config
from camera import CameraError, check_reachable, open_capture, validate_url
from motion import MotionDetector
from overlay import FpsMeter, draw_overlay, put_label, resize_keep_aspect
from recorder import Recorder, save_screenshot

logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
)

WINDOW = "IP Camera Viewer"
ESC = 27
MAX_FAILED_READS = 10
MESSAGE_SECONDS = 2.0
MOTION_MIN_AREA = 800
MOTION_FRAMES_TO_START = 3
MOTION_STOP_AFTER = 5.0


class ViewerState:
    """Hold the transient state that the loop shares with key handling."""

    def __init__(self) -> None:
        self.message = ""
        self.message_until = 0.0
        self.motion_enabled = False
        self.manual_recording = False
        self.motion_hits = 0
        self.last_motion_at = None
        self.boxes: list[tuple[int, int, int, int]] = []

    def set_message(self, text: str, seconds: float = MESSAGE_SECONDS) -> None:
        self.message = text
        self.message_until = time.time() + seconds

    def message_active(self) -> bool:
        return time.time() < self.message_until


def process_frame(frame, fps: float, recorder: Recorder, state: ViewerState):
    """Draw status after media is written, so saved files stay clean."""
    draw_overlay(frame, config.CAMERA_NAME, fps)
    recorder.write(frame)
    display = frame
    if recorder.recording or state.message_active() or state.motion_enabled:
        display = frame.copy()
    if state.motion_enabled:
        for x, y, w, h in state.boxes:
            cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)
    if recorder.recording:
        x = display.shape[1] - 120
        cv2.circle(display, (x, 25), 8, (0, 0, 255), -1)
        put_label(display, f"REC {recorder.elapsed()}s", (x + 14, 25))
    if state.message_active():
        put_label(display, state.message, (10, 80))
    return display


def handle_keys(key: int, frame, recorder: Recorder, fps: float, state: ViewerState) -> bool:
    """Apply one key press and report whether the loop should stop."""
    if key == ESC:
        return True
    if key in (ord("s"), ord("S")):
        try:
            path = save_screenshot(frame)
            state.set_message(f"Screenshot saved: {os.path.basename(path)}")
        except OSError as exc:
            state.set_message(str(exc))
        return False
    if key in (ord("r"), ord("R")):
        if recorder.recording:
            recorder.stop()
            state.manual_recording = False
            state.set_message("Recording saved")
        else:
            try:
                recorder.start(frame, fps)
                state.manual_recording = True
                state.set_message("Recording started")
            except OSError as exc:
                state.set_message(str(exc))
        return False
    if key in (ord("m"), ord("M")):
        state.motion_enabled = not state.motion_enabled
        state.boxes = []
        state.set_message("Motion on" if state.motion_enabled else "Motion off")
    return False


def reconnect(cap, url: str, max_attempts: int, delay: float):
    """Release the old capture and retry a bounded number of times."""
    cap.release()
    for attempt in range(1, max_attempts + 1):
        print(f"Connection lost. Reconnecting ({attempt}/{max_attempts})...", file=sys.stderr)
        if cv2.waitKey(int(delay * 1000)) & 0xFF == ESC:
            raise KeyboardInterrupt
        try:
            check_reachable(url, config.REQUEST_TIMEOUT, config.CAMERA_VERIFY_SSL)
            return open_capture(url, verify_ssl=config.CAMERA_VERIFY_SSL)
        except CameraError:
            continue
    raise CameraError(f"Could not reconnect after {max_attempts} attempts. Giving up.")


def main() -> int:
    """Run the viewer until Esc, Ctrl+C, window close or an unrecoverable error."""
    cap = None
    recorder = None
    exit_code = 0
    try:
        url = validate_url(config.CAMERA_URL)
        check_reachable(url, config.REQUEST_TIMEOUT, config.CAMERA_VERIFY_SSL)
        cap = open_capture(url, verify_ssl=config.CAMERA_VERIFY_SSL)
        recorder = Recorder()
        fps_meter = FpsMeter()
        detector = MotionDetector(MOTION_MIN_AREA)
        state = ViewerState()
        failed_reads = 0
        last_display = None
        print("Viewer started. Camera address hidden. Press Esc to quit.")
        while True:
            ok, frame = cap.read()
            if not ok:
                failed_reads += 1
                if failed_reads < MAX_FAILED_READS:
                    if cv2.waitKey(1) & 0xFF == ESC:
                        raise KeyboardInterrupt
                    continue
                if recorder.recording:
                    recorder.stop()
                    state.manual_recording = False
                if last_display is not None:
                    notice = last_display.copy()
                    put_label(notice, "Reconnecting...", (10, 110))
                    cv2.imshow(WINDOW, notice)
                cap = reconnect(cap, url, config.MAX_RECONNECTS, config.RECONNECT_DELAY)
                failed_reads = 0
                continue

            failed_reads = 0
            frame = resize_keep_aspect(frame, config.DISPLAY_WIDTH)
            fps = fps_meter.tick()

            if state.motion_enabled:
                state.boxes = detector.detect(frame)
                if state.boxes:
                    state.last_motion_at = time.monotonic()
                    if not recorder.recording and not state.manual_recording:
                        state.motion_hits += 1
                        if state.motion_hits >= MOTION_FRAMES_TO_START:
                            try:
                                recorder.start(frame, fps)
                                state.set_message("Recording started by motion")
                            except OSError as exc:
                                state.set_message(str(exc))
                            state.motion_hits = 0
                else:
                    state.motion_hits = 0
                if (
                    recorder.recording
                    and not state.manual_recording
                    and state.last_motion_at
                    and time.monotonic() - state.last_motion_at > MOTION_STOP_AFTER
                ):
                    recorder.stop()
                    state.last_motion_at = None
                    state.set_message("Motion recording saved")

            display = process_frame(frame, fps, recorder, state)
            cv2.imshow(WINDOW, display)
            last_display = display
            try:
                if cv2.getWindowProperty(WINDOW, cv2.WND_PROP_VISIBLE) < 1:
                    break
            except cv2.error:
                break
            if handle_keys(cv2.waitKey(1) & 0xFF, frame, recorder, fps, state):
                break
    except CameraError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        exit_code = 1
    except KeyboardInterrupt:
        print("Interrupted, shutting down.")
    except Exception:
        logging.exception("Unexpected error")
        print("Unexpected error, see app.log", file=sys.stderr)
        exit_code = 1
    finally:
        if recorder is not None:
            recorder.stop()
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()
    return exit_code


if __name__ == "__main__":
    sys.exit(main())

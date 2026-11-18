"""Write screenshots and recordings with names that never collide.

Issue #4; TC06, TC07, TC09 and TC10; technical questions 13, 14 and 15.
See ADR-0004 (processing order) and ADR-0008 (file names).
"""

import os
from datetime import datetime

import cv2


def timestamped_path(folder: str, prefix: str, ext: str) -> str:
    """Build a path with millisecond resolution and a collision suffix."""
    os.makedirs(folder, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    path = os.path.join(folder, f"{prefix}_{stamp}.{ext}")
    n = 1
    while os.path.exists(path):
        path = os.path.join(folder, f"{prefix}_{stamp}_{n}.{ext}")
        n += 1
    return path


def save_screenshot(frame, folder: str = "screenshots") -> str:
    """Save one frame as a JPEG and return its path."""
    path = timestamped_path(folder, "shot", "jpg")
    if not cv2.imwrite(path, frame):
        raise OSError("Could not write the screenshot.")
    return path


class Recorder:
    """Write one recording at a time through OpenCV VideoWriter."""

    def __init__(self, folder: str = "recordings"):
        self.folder = folder
        self.writer = None
        self.path = None
        self.started_at = None
        self.size = None

    @property
    def recording(self) -> bool:
        return self.writer is not None

    def start(self, frame, fps: float) -> None:
        """Start a recording sized to the frame it is given."""
        h, w = frame.shape[:2]
        self.size = (w, h)
        self.path = timestamped_path(self.folder, "rec", "mp4")
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        rate = min(max(round(fps), 5), 30) if fps else 15
        self.writer = cv2.VideoWriter(self.path, fourcc, rate, self.size)
        if not self.writer.isOpened():
            self.writer = None
            raise OSError("Could not start the recording (codec or folder problem).")
        self.started_at = datetime.now()

    def write(self, frame) -> None:
        """Append a frame whose size matches the declared size."""
        if self.writer is not None:
            self.writer.write(frame)

    def elapsed(self) -> int:
        """Return whole seconds since the recording started."""
        if self.started_at is None:
            return 0
        return int((datetime.now() - self.started_at).total_seconds())

    def stop(self) -> str | None:
        """Finalise the file and return its path, or None when idle."""
        path = self.path
        if self.writer is not None:
            self.writer.release()
        self.writer = self.path = self.started_at = None
        return path

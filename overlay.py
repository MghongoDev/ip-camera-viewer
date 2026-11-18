"""Resize frames and draw the four overlays.

Issue #3; TC04 and TC05; technical questions 7, 11 and 12.
See ADR-0006 (hand-written helpers).
"""

import time
from datetime import datetime

import cv2

FONT = cv2.FONT_HERSHEY_SIMPLEX


def resize_keep_aspect(frame, target_width: int):
    """Scale a frame to a fixed width and keep its aspect ratio."""
    h, w = frame.shape[:2]
    if w == target_width:
        return frame
    scale = target_width / w
    new_h = int(h * scale) // 2 * 2
    return cv2.resize(frame, (target_width, new_h), interpolation=cv2.INTER_AREA)


class FpsMeter:
    """Estimate FPS from the gap between frames, smoothed so the number is readable."""

    def __init__(self, smoothing: float = 0.1):
        self.alpha = smoothing
        self.fps = 0.0
        self._prev = None

    def tick(self) -> float:
        now = time.perf_counter()
        if self._prev is not None and now > self._prev:
            instant = 1.0 / (now - self._prev)
            self.fps = instant if self.fps == 0 else self.alpha * instant + (1 - self.alpha) * self.fps
        self._prev = now
        return self.fps


def put_label(img, text: str, org, scale: float = 0.6) -> None:
    """Draw white text on a dark box so it reads on any scene."""
    (tw, th), base = cv2.getTextSize(text, FONT, scale, 1)
    x, y = org
    cv2.rectangle(img, (x - 4, y - th - 4), (x + tw + 4, y + base), (0, 0, 0), -1)
    cv2.putText(img, text, org, FONT, scale, (255, 255, 255), 1, cv2.LINE_AA)


def draw_overlay(frame, camera_name: str, fps: float) -> None:
    """Draw timestamp, camera name, resolution and FPS onto the frame."""
    h, w = frame.shape[:2]
    put_label(frame, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), (10, 25))
    put_label(frame, camera_name, (10, 50))
    put_label(frame, f"{w}x{h}", (10, h - 35))
    put_label(frame, f"FPS: {fps:4.1f}", (10, h - 10))

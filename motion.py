"""Detect movement with frame differencing for the bonus feature.

Bonus 7a of the implementation guide. See ADR-0007 (motion shares the recorder).
"""

import cv2


class MotionDetector:
    """Find regions that changed since the previous frame."""

    def __init__(self, min_area: int = 800):
        self.min_area = min_area
        self._prev = None

    def detect(self, frame) -> list[tuple[int, int, int, int]]:
        """Return bounding boxes of changed regions as (x, y, w, h)."""
        gray = cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (21, 21), 0)
        if self._prev is None:
            self._prev = gray
            return []
        delta = cv2.absdiff(self._prev, gray)
        self._prev = gray
        mask = cv2.dilate(cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1], None, iterations=2)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return [cv2.boundingRect(c) for c in contours if cv2.contourArea(c) >= self.min_area]

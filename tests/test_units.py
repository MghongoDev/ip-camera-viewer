"""Unit tests for the pure helpers, run with python -m unittest discover -s tests."""

import os
import tempfile
import unittest

import numpy as np

from camera import CameraError, validate_url
from overlay import FpsMeter, resize_keep_aspect
from recorder import Recorder, save_screenshot, timestamped_path


class ValidateUrlTests(unittest.TestCase):
    def test_empty_url(self):
        with self.assertRaises(CameraError):
            validate_url("")

    def test_bad_scheme(self):
        with self.assertRaises(CameraError):
            validate_url("hello")

    def test_https_url_accepted(self):
        url = "https://192.0.2.10:8080/video"
        self.assertEqual(validate_url(url), url)


class OverlayTests(unittest.TestCase):
    def test_resize_keeps_aspect(self):
        frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
        out = resize_keep_aspect(frame, 960)
        self.assertEqual(out.shape, (540, 960, 3))

    def test_resize_same_width_returns_input(self):
        frame = np.zeros((480, 960, 3), dtype=np.uint8)
        self.assertIs(resize_keep_aspect(frame, 960), frame)

    def test_fps_meter_starts_at_zero(self):
        self.assertEqual(FpsMeter().fps, 0.0)


class RecorderTests(unittest.TestCase):
    def test_timestamped_path_is_unique(self):
        with tempfile.TemporaryDirectory() as folder:
            first = timestamped_path(folder, "rec", "mp4")
            open(first, "w").close()
            second = timestamped_path(folder, "rec", "mp4")
            self.assertNotEqual(first, second)

    def test_save_screenshot(self):
        with tempfile.TemporaryDirectory() as folder:
            frame = np.zeros((120, 160, 3), dtype=np.uint8)
            path = save_screenshot(frame, folder)
            self.assertTrue(os.path.getsize(path) > 0)

    def test_recorder_finalises_file(self):
        with tempfile.TemporaryDirectory() as folder:
            rec = Recorder(folder)
            frame = np.zeros((120, 160, 3), dtype=np.uint8)
            rec.start(frame, 15)
            self.assertTrue(rec.recording)
            rec.write(frame)
            path = rec.stop()
            self.assertIsNotNone(path)
            self.assertFalse(rec.recording)
            self.assertTrue(os.path.getsize(path) > 0)


if __name__ == "__main__":
    unittest.main()

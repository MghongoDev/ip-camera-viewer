"""Read settings from the environment and expose them as module constants.

Issue #1. See ADR-0001 (secrets) and ADR-0005 (TLS).
"""

import os

from dotenv import load_dotenv

load_dotenv()

CAMERA_URL = os.getenv("CAMERA_URL", "").strip()
CAMERA_NAME = os.getenv("CAMERA_NAME", "Camera 1")
DISPLAY_WIDTH = int(os.getenv("DISPLAY_WIDTH", "960"))
MAX_RECONNECTS = int(os.getenv("MAX_RECONNECTS", "5"))
RECONNECT_DELAY = float(os.getenv("RECONNECT_DELAY", "2"))
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "5"))
CAMERA_VERIFY_SSL = os.getenv("CAMERA_VERIFY_SSL", "false").strip().lower() in {
    "1",
    "true",
    "yes",
}

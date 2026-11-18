"""Validate the camera address and open the stream without hanging.

Issues #2 and #5; TC02, TC03 and TC08.
See ADR-0002 (reachability probe) and ADR-0005 (self-signed TLS).
"""

import os
from urllib.parse import urlparse

import cv2
import requests

try:
    from urllib3.exceptions import InsecureRequestWarning
except ImportError:  # urllib3 ships with requests, but keep older installs working
    InsecureRequestWarning = None


class CameraError(Exception):
    """A camera problem we can explain to the user in one sentence."""


def validate_url(url: str) -> str:
    """Return the URL after checking its scheme and host."""
    if not url:
        raise CameraError("No camera URL set. Copy .env.example to .env and set CAMERA_URL.")
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https", "rtsp") or not parsed.hostname:
        raise CameraError("The camera URL is not valid. Expected https://<ip>:8080/video")
    return url


def check_reachable(url: str, timeout: float = 5, verify_ssl: bool = True) -> None:
    """Fail fast before OpenCV sees an address that may never answer."""
    if url.startswith("rtsp"):
        return
    if not verify_ssl and InsecureRequestWarning is not None:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    try:
        with requests.get(url, stream=True, timeout=timeout, verify=verify_ssl) as resp:
            if resp.status_code in (401, 403):
                raise CameraError("The camera rejected the login. Check the credentials in the URL.")
            resp.raise_for_status()
    except requests.exceptions.Timeout as exc:
        raise CameraError("The camera did not answer in time. Is the app running on the same Wi-Fi?") from exc
    except requests.exceptions.ConnectionError as exc:
        raise CameraError("Cannot reach the camera. Check the address, port and Wi-Fi.") from exc
    except requests.exceptions.SSLError as exc:
        raise CameraError(
            "The camera uses a self-signed certificate. Set CAMERA_VERIFY_SSL=false in .env."
        ) from exc
    except requests.exceptions.HTTPError as exc:
        raise CameraError(f"The camera returned {exc.response.status_code} for the video path.") from exc
    except requests.exceptions.RequestException as exc:
        raise CameraError(f"Camera check failed: {type(exc).__name__}") from exc


def open_capture(url: str, timeout_ms: int = 5000, verify_ssl: bool = True) -> cv2.VideoCapture:
    """Open the stream with short timeouts and the requested TLS policy."""
    if url.startswith("https") and not verify_ssl:
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "tls_verify;0"
    params = []
    for name in ("CAP_PROP_OPEN_TIMEOUT_MSEC", "CAP_PROP_READ_TIMEOUT_MSEC"):
        prop = getattr(cv2, name, None)
        if prop is not None:
            params.extend([prop, timeout_ms])
    if params and hasattr(cv2, "CAP_FFMPEG"):
        cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG, params)
    else:
        cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        cap.release()
        raise CameraError("The stream could not be opened. Check the video path in the camera URL.")
    return cap

# Integration test results

Date: 18 November 2026

The ten integration tests (TC01 to TC10) come from Phase 6 of the implementation guide. This host has no GUI camera session and no reachable phone stream, so only the two tests that need no camera could run. TC02 and TC03 passed with a clean one-line error and exit code 1. TC01 and TC04 to TC10 are marked Not run; each row states the exact step to run it on the phone. No evidence image was captured on this host, and no evidence file name is listed here. The camera address never appears in console output or evidence.

## Results

| ID | Test | What was done | Expected | Actual | Evidence | Result |
|---|---|---|---|---|---|---|
| TC01 | Live stream starts | Not done. To run: start IP Webcam on the phone, set `CAMERA_URL` in `.env` to the address the app shows with `/video` appended, then run `python main.py` in a desktop session and watch for live video. | Live video within a few seconds; `Esc` closes the window and the terminal returns with no traceback. | Not observed on this host. | Not captured. | Not run |
| TC02 | Invalid URL | Ran `python main.py` with an invalid `CAMERA_URL` value. | Clear one-line error, clean exit with code 1, no traceback. | `CameraError` invalid-URL message beginning `The camera URL is not valid.` printed to stderr; exit code 1; no traceback. | Console output from this run. No image file captured. | Pass |
| TC03 | Camera unavailable | Ran `python main.py` with an unreachable phone address so the HTTP GET timed out. | Reports unreachable within `REQUEST_TIMEOUT` (5 s), no hang, clean exit with code 1. | Timeout message `The camera did not answer in time. Is the app running on the same Wi-Fi?` printed to stderr; exit code 1; no traceback. | Console output from this run. No image file captured. | Pass |
| TC04 | Overlays | Not done. To run: start the stream, then watch the window for 30 seconds. | Timestamp updates each second; camera name, resolution and FPS stay readable. | Not observed on this host. | Not captured. | Not run |
| TC05 | Resizing | Not done. To run: start the stream and compare the window width with `DISPLAY_WIDTH` (960); a 1920x1080 source should show as 960x540. | Width 960, aspect ratio kept, circles stay round. | Not observed on this host. | Not captured. | Not run |
| TC06 | Screenshot | Not done. To run: start the stream, press `S` twice a few seconds apart, then list `screenshots/`. | Two different timestamped JPEG files and a confirmation on screen each time. | Not observed on this host. | Not captured. | Not run |
| TC07 | Recording | Not done. To run: press `R`, wait about 10 seconds, press `R` again, then play the file in a media player. | REC badge shown; file plays; duration about 10 seconds at natural speed. | Not observed on this host. | Not captured. | Not run |
| TC08 | Connection drop | Not done. To run: start the stream, turn the phone Wi-Fi off for 10 seconds and back on, then watch the window. | Reports the drop, retries, then recovers or exits cleanly at the limit. | Not observed on this host. | Not captured. | Not run |
| TC09 | Esc during recording | Not done. To run: press `R`, wait a few seconds, press `Esc`, then play the saved file. | Window closes, file saved and plays, camera released. | Not observed on this host. | Not captured. | Not run |
| TC10 | Ctrl+C during recording | Not done. To run: press `R`, wait a few seconds, press `Ctrl+C` in the terminal, then play the saved file. | No traceback, file saved and plays, camera released. | Not observed on this host. | Not captured. | Not run |

## Unit tests

The command `python -m unittest discover -s tests` ran 9 tests and all passed. The suite covers `validate_url` (empty URL, bad scheme, accepted https URL), `resize_keep_aspect` (aspect ratio, same-width shortcut), `FpsMeter` (starts at zero), `timestamped_path` (unique names), `save_screenshot` (non-empty file) and `Recorder` (file finalised and writer cleared on stop). This result is separate from TC01 to TC10, which need a camera.

## Running the GUI tests on the phone

First set up the camera. Install IP Webcam on the phone and connect the phone and laptop to the same ordinary Wi-Fi, not mobile data and not a guest network that isolates clients. Start the server in the app. Copy `.env.example` to `.env` and set `CAMERA_URL` to the address the app shows with `/video` appended. Keep the phone screen on and the app in the foreground. Run the viewer from a desktop session with `python main.py`. On Wayland, set `QT_QPA_PLATFORM=xcb` first if OpenCV reports a Qt xcb plugin error. The "What was done" column above gives the action for each test. After each test, record the result and capture the evidence described below.

## Capturing evidence without exposing the address

Evidence screenshots must never reveal the camera address, port or credentials. Crop the image to the OpenCV window and to the console lines that matter. Hide terminal history and any `.env` content before recording. Blur or crop any line that shows an IP address, a URL, a port or a password. The viewer prints only "Viewer started. Camera address hidden." or a one-line error, so the window and those messages are safe to show. Check the finished image before attaching it, and keep captured media out of tracked folders.

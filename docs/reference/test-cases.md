# Test cases

This page lists the ten integration cases from the implementation guide and the nine unit tests in `tests/test_units.py`. Each case has an intent and an expected result. The execution status is stated so no result is read as evidence that was not collected. Terms such as "failed read" and "test evidence" are defined in [GLOSSARY.md](../../GLOSSARY.md).

## Execution status in this environment

- 9 unit tests were run with `python -m unittest discover -s tests`. All 9 pass.
- `TC02` and `TC03` were executed. Both exit with code 1 and a clean one-line message.
- `TC01` and `TC04` through `TC10` were not executed here. They need a phone running IP Webcam on the same Wi-Fi and a live graphical window.
- No evidence screenshots are stored in this checkout. The guide puts them in `docs/tests/`, which does not exist here. Any evidence captured later must hide the camera address and credentials.

## Integration cases

| ID | Intent | Expected result | Executed here | Result |
|---|---|---|---|---|
| `TC01` | Start with a correct camera URL. | Live video appears in the OpenCV window within a few seconds. | No | Not run. |
| `TC02` | Start with an invalid URL such as `http://camera` or an empty value. | Clear error, clean exit, no traceback. | Yes | Exit code 1 with a clean message. |
| `TC03` | Start with the phone app stopped or an unreachable address. | Unreachable reported quickly, no hang, clean exit. | Yes | Exit code 1 with a clean message. |
| `TC04` | Watch the overlay for 30 seconds. | Timestamp updates each second. Name, resolution and FPS stay readable. | No | Not run. |
| `TC05` | Compare the window and saved frame with `DISPLAY_WIDTH`. | Width equals `960`; aspect ratio kept. | No | Not run. |
| `TC06` | Press `S` twice. | Two timestamped JPEG files and a confirmation after each press. | No | Not run. |
| `TC07` | Press `R`, wait about 10 seconds, press `R` again. | REC badge shown; MP4 plays at natural speed for about 10 seconds. | No | Not run. |
| `TC08` | Turn the phone Wi-Fi off for 10 seconds, then back on. | Drop reported, retries run, then recovery or a clean exit at the limit. | No | Not run. |
| `TC09` | Start a recording, then press `Esc`. | Window closes, file saved and playable, capture released. | No | Not run. |
| `TC10` | Start a recording, then press `Ctrl+C`. | No traceback, file saved and playable, camera released. | No | Not run. |

## Unit tests

Run from the project root: `python -m unittest discover -s tests`. All nine pass.

| Test | Intent |
|---|---|
| `ValidateUrlTests.test_empty_url` | An empty `CAMERA_URL` raises `CameraError`. |
| `ValidateUrlTests.test_bad_scheme` | `hello` raises `CameraError`. |
| `ValidateUrlTests.test_https_url_accepted` | An `https` URL with a hostname is returned unchanged. |
| `OverlayTests.test_resize_keeps_aspect` | A `1920x1080` frame resized to width `960` becomes `960x540`. |
| `OverlayTests.test_resize_same_width_returns_input` | Resizing to the existing width returns the same array object. |
| `OverlayTests.test_fps_meter_starts_at_zero` | A fresh `FpsMeter` reports `0.0`. |
| `RecorderTests.test_timestamped_path_is_unique` | A second path is different when the first file exists. |
| `RecorderTests.test_save_screenshot` | A saved screenshot has a nonzero size. |
| `RecorderTests.test_recorder_finalises_file` | Start, write and stop leaves a nonzero file and clears the recording state. |

## Related decisions

- [ADR-0003](../adr/0003-bound-the-reconnect.md) sets the retry limits exercised by `TC08`.
- [ADR-0004](../adr/0004-write-media-before-status-drawing.md) fixes the content checked by `TC06` and `TC07`.
- [ADR-0008](../adr/0008-name-media-with-milliseconds.md) fixes the file names checked by `TC06`.

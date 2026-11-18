# Module map

Seven Python files make up the viewer. `main.py` owns the loop and imports the others. The imported modules do not import each other. This keeps each helper testable on its own. See [GLOSSARY.md](../../GLOSSARY.md) for domain words.

## Python modules

| File | Role | Public names | Imports from project |
|---|---|---|---|
| `../../main.py` | Entry point, main loop, key handling, reconnect, safe shutdown. | `ViewerState`, `process_frame`, `handle_keys`, `reconnect`, `main`, seven constants. | `config`, `camera`, `motion`, `overlay`, `recorder` |
| `../../config.py` | Reads `.env` and exposes settings as module constants. | `CAMERA_URL`, `CAMERA_NAME`, `DISPLAY_WIDTH`, `MAX_RECONNECTS`, `RECONNECT_DELAY`, `REQUEST_TIMEOUT`, `CAMERA_VERIFY_SSL`. | none |
| `../../camera.py` | Validates the address, probes reachability, opens the capture. | `CameraError`, `validate_url`, `check_reachable`, `open_capture`. | none |
| `../../overlay.py` | Resizes frames, estimates FPS, draws the overlay. | `FONT`, `resize_keep_aspect`, `FpsMeter`, `put_label`, `draw_overlay`. | none |
| `../../recorder.py` | Builds file names, writes screenshots, manages one recording. | `timestamped_path`, `save_screenshot`, `Recorder`. | none |
| `../../motion.py` | Finds changed regions with frame differencing. | `MotionDetector`. | none |
| `../../tests/test_units.py` | Nine unit tests for the pure helpers. | `ValidateUrlTests`, `OverlayTests`, `RecorderTests`. | `camera`, `overlay`, `recorder` |

## Import direction

`main.py` sits at the top. It calls `validate_url`, `check_reachable` and `open_capture` before the loop. Inside the loop it calls `resize_keep_aspect`, `FpsMeter.tick`, `MotionDetector.detect`, `process_frame` and `handle_keys`. `process_frame` calls `draw_overlay`, `put_label` and `Recorder.write`. `handle_keys` calls `save_screenshot` and the `Recorder` start and stop methods.

`config.py`, `camera.py`, `overlay.py`, `recorder.py` and `motion.py` depend only on the standard library, OpenCV, NumPy or Requests. No cycle exists.

## Support files

| File | Role |
|---|---|
| `../../requirements.txt` | Pinned packages: `opencv-python==5.1.0.95`, `numpy==2.5.5`, `requests==2.34.2`, `python-dotenv==1.2.4`. Pins need Python 3.12+ because of numpy; source runs on 3.10+ with older pins. |
| `../../.env.example` | Committed template with placeholders only. Uses `https://<phone-ip>:8080/video`. |
| `.env` | Local real settings. Not committed. |
| `../../.gitignore` | Excludes `.env`, `.venv/`, `__pycache__/`, `recordings/`, `screenshots/`, `*.log`, editor files and the untracked implementation guide. |
| `../adr/` | Nine accepted ADRs, numbered `0001` to `0009`. |
| `app.log` | Error-level log written by the outer `except Exception` handler. Gitignored. |

## Data locations

| Path | Written by | Content |
|---|---|---|
| `screenshots/` | `save_screenshot` | JPEG frames named `shot_{milliseconds}.jpg`. |
| `recordings/` | `Recorder.start` | MP4 files named `rec_{milliseconds}.mp4`. |
| `app.log` | `logging.basicConfig` in `main.py` | Tracebacks for unexpected errors. |

Each folder is created on demand. All three are excluded from Git.

## Related decisions

- [ADR-0006](../adr/0006-write-resize-and-fps-helpers.md) keeps the resize and FPS math in `overlay.py`.
- [ADR-0007](../adr/0007-share-the-motion-path.md) makes motion use the existing recorder.
- [ADR-0008](../adr/0008-name-media-with-milliseconds.md) fixes the file naming scheme.
- [ADR-0009](../adr/0009-use-the-divio-four-part-layout.md) fixes the documentation layout.

# Configuration

Settings come from two places. Values that users change live in `.env` and load through `config.py`. Values that fix the program's limits live as constants in `main.py`. This page lists both sets with their defaults. Terms such as "reachability probe" and "reconnect" are defined in [GLOSSARY.md](../../GLOSSARY.md).

## Environment settings

`config.py` reads `.env` with `python-dotenv`. `load_dotenv()` does not overwrite a variable that is already set in the environment, so an exported environment value takes precedence over the file. The table shows the default used when a name is absent.

| Name | Default | Type | Purpose |
|---|---|---|---|
| `CAMERA_URL` | empty string | string | Full stream address: scheme, `https://<phone-ip>:8080/video`, port and `/video` path. Required. |
| `CAMERA_NAME` | `Camera 1` | string | Label drawn in the overlay. |
| `DISPLAY_WIDTH` | `960` | int | Width in pixels of the displayed and saved frame. Height follows from the aspect ratio. |
| `MAX_RECONNECTS` | `5` | int | Number of reconnect attempts after the failed-read limit is reached. |
| `RECONNECT_DELAY` | `2` | float | Seconds between reconnect attempts. Also the length of the `waitKey` call that keeps the window responsive during a wait. |
| `REQUEST_TIMEOUT` | `5` | float | Seconds allowed for the reachability probe before it reports a timeout. |
| `CAMERA_VERIFY_SSL` | `false` | bool | Controls TLS verification in both the probe and the FFmpeg capture. |

### Boolean parsing

`CAMERA_VERIFY_SSL` is a string in the file. `config.py` strips whitespace, lowercases it, and treats `1`, `true` and `yes` as true. Every other value, including the empty string, is false.

### Camera URL

`validate_url` accepts `http`, `https` and `rtsp` schemes and requires a hostname. An empty value, `hello` and an `ftp` address fail with a `CameraError`. An address such as `http://camera` passes validation and fails later at the reachability probe. Both paths produce a one-line message and exit code 1. Use `https://<phone-ip>:8080/video` in `.env`.

### TLS setting

`CAMERA_VERIFY_SSL` defaults to `false` because IP Webcam serves a certificate the phone signs itself. When the value is false, `check_reachable` suppresses the `InsecureRequestWarning` and calls `requests.get` with `verify=False`. `open_capture` sets `OPENCV_FFMPEG_CAPTURE_OPTIONS=tls_verify;0` before opening an HTTPS stream. See [ADR-0005](../adr/0005-handle-the-self-signed-certificate.md) for the reason.

## Constants in main.py

These values are hard-coded. `.env` does not change them.

| Name | Value | Purpose |
|---|---|---|
| `WINDOW` | `"IP Camera Viewer"` | Title of the OpenCV window. |
| `ESC` | `27` | Key code that stops the loop. |
| `MAX_FAILED_READS` | `10` | Consecutive failed `cap.read()` calls tolerated before reconnecting. |
| `MESSAGE_SECONDS` | `2.0` | Seconds a status message stays on screen. |
| `MOTION_MIN_AREA` | `800` | Smallest contour area that counts as motion. |
| `MOTION_FRAMES_TO_START` | `3` | Consecutive frames with motion before auto-record starts. |
| `MOTION_STOP_AFTER` | `5.0` | Seconds without motion before auto-record stops. |

Two more constants are defaults in other modules: `MotionDetector` uses `min_area=800`, and `FpsMeter` uses `smoothing=0.1`. The recorder clamps the video rate to 5 to 30 frames per second and uses 15 when the measured rate is zero.

## Related decisions

- [ADR-0001](../adr/0001-keep-camera-secrets-out-of-git.md) keeps the real address out of Git.
- [ADR-0005](../adr/0005-handle-the-self-signed-certificate.md) explains the TLS default.

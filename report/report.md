# IP Camera Viewer report

Project: IP Camera Viewer
Date: 18 November 2026
GitHub repository: https://github.com/MghongoDev/ip-camera-viewer

## Overview

IP Camera Viewer is a Python and OpenCV desktop program. It reads the stream from an Android phone running IP Webcam on the same Wi-Fi and shows it in a window. Four overlays sit on every frame: timestamp, camera name, resolution and frames per second. The `S` key saves a JPEG screenshot. The `R` key starts and stops an MP4 recording. The `M` key toggles bonus motion detection with auto-record. `Esc` quits. A reachability probe runs before OpenCV, and a bounded reconnect handles a dropped stream.

Use only a camera you own or have permission to use. Record only places and people who agreed. Video of identifiable people is personal data. Keep files local, keep the camera address out of Git and evidence, and delete recordings you no longer need. The viewer never prints the address; it prints only "Viewer started. Camera address hidden." Every evidence screenshot must be cropped or blurred so no address, port or credential appears.

## Design

### Architecture

The phone serves an MJPEG stream over HTTP or HTTPS on the local network. `config.py` reads `CAMERA_URL`, `CAMERA_NAME`, `DISPLAY_WIDTH`, `MAX_RECONNECTS`, `RECONNECT_DELAY`, `REQUEST_TIMEOUT` and `CAMERA_VERIFY_SSL` from the environment. `camera.py` validates the address, probes it with Requests, and opens it with OpenCV. `main.py` runs one loop that reads, resizes, measures FPS, writes media, draws overlays, shows the frame and handles keys. `overlay.py` and `recorder.py` do the frame and file work. `motion.py` supplies the bonus detector.

```
Phone (IP Webcam, HTTPS/Wi-Fi) --> camera.py (validate, probe, open, reconnect)
                                      | frames: NumPy uint8, BGR
 .env --> config.py --> main.py (one loop)
                                      |--> overlay.py  (resize, four labels, FPS)
                                      |--> recorder.py (VideoWriter, screenshots)
                                      |--> motion.py   (bonus boxes)
                                      --> cv2.imshow + cv2.waitKey --> Esc / S / R / M
```

ADRs record the non-obvious choices: keep secrets out of Git (0001), probe before OpenCV (0002), bound the reconnect (0003), write media before status drawing (0004), handle the self-signed certificate (0005), write resize and FPS helpers locally (0006), share one path for the two bonus items (0007), name media with milliseconds (0008), and use the Divio four-part documentation layout (0009).

### Modules

`config.py` calls `load_dotenv()` and exposes settings as module constants. `CAMERA_URL` defaults to an empty string, `DISPLAY_WIDTH` to 960, `MAX_RECONNECTS` to 5, `RECONNECT_DELAY` to 2, `REQUEST_TIMEOUT` to 5 and `CAMERA_VERIFY_SSL` to false. The real address stays in `.env`, which Git ignores.

`camera.py` defines `CameraError` and three helpers. `validate_url` accepts only http, https and rtsp schemes with a host. `check_reachable` sends `requests.get(url, stream=True, timeout=..., verify=...)`, checks 401 and 403, calls `raise_for_status()`, and maps Timeout, ConnectionError, SSLError and other request failures to one-line messages. It skips RTSP. `open_capture` opens with `cv2.CAP_FFMPEG` and open/read timeouts of 5000 ms, sets `OPENCV_FFMPEG_CAPTURE_OPTIONS=tls_verify;0` for HTTPS when verification is off, and checks `isOpened()`. ADR-0005 explains the certificate trade-off.

`overlay.py` holds `resize_keep_aspect`, `FpsMeter`, `put_label` and `draw_overlay`. Resizing keeps the aspect ratio and rounds the new height down to an even number. `FpsMeter` uses `time.perf_counter()` and an exponential moving average with alpha 0.1. `put_label` draws white text on a dark box. `draw_overlay` places timestamp, name, resolution and FPS. The calculations stay in the code so they can be answered directly (ADR-0006).

`recorder.py` holds `timestamped_path`, `save_screenshot` and the `Recorder` class. `timestamped_path` uses a millisecond stamp and a numeric suffix so files never collide. `save_screenshot` writes a JPEG and raises `OSError` on failure. `Recorder` writes one MP4 at a time with the `mp4v` codec, sizes it from the resized frame, clamps the rate to 5 through 30, and finalises the file in `stop()`.

`motion.py` holds `MotionDetector`. It converts the frame to grayscale, blurs it, takes the absolute difference from the previous frame, thresholds at 25, dilates twice and returns bounding boxes with area at least `min_area`, which defaults to 800.

`main.py` owns the loop, key handling, reconnect and cleanup. `ViewerState` holds transient state. `process_frame` draws the four overlays, writes the frame to any active recording, then copies the frame only when a REC badge, message or motion box must be drawn. `handle_keys` maps Esc, S, R and M. `reconnect` releases the old capture and retries. The `finally` block stops the recorder, releases the capture and destroys the windows on every exit path.

## Features

The live view opens within a few seconds of a correct URL and closes cleanly on Esc, Ctrl+C or the window close button. Frames are resized to a 960-pixel width with the aspect ratio kept, so circles stay round. The four overlays update each frame; the timestamp changes once a second and the smoothed FPS stays readable.

Pressing `S` writes a `shot_` JPEG into `screenshots/`, named with a millisecond timestamp, from the frame before status decoration, and shows a two-second confirmation. Pressing `R` writes a `rec_` MP4 into `recordings/` with the same naming scheme; the red REC dot and elapsed seconds show while it runs, and a second press stops it. Files use millisecond names so two quick presses stay separate.

Bad addresses and timeouts produce a one-line message and exit code 1. A run of 10 failed reads triggers up to 5 reconnect attempts 2 seconds apart; the last frame shows "Reconnecting..." during the wait. `M` toggles motion detection; green boxes mark changed regions and motion can start a recording that stops about 5 seconds after movement ends. A manual recording always takes priority.

## Test results

Ten integration tests are defined in the implementation guide. On this host only `TC02` (invalid URL) and `TC03` (camera unavailable, timeout) could run, because there is no GUI camera session and no reachable phone stream. Both passed with a clean one-line error and exit code 1. The other eight tests need a phone on the same Wi-Fi and a desktop session; they are marked Not run. The full record, including the exact step for each test, is in `docs/tests/RESULTS.md`. The unit suite `python -m unittest discover -s tests` ran 9 tests and all passed.

## Technical Questions

### Part A: Python and networking

1. An IP address identifies a device on a network. IP Webcam gives the phone a private address such as `192.168.x.x`, which only devices on the same local network can reach. `CAMERA_URL` in `.env` holds that address behind the `<phone-ip>` placeholder. `validate_url` in `camera.py` checks the scheme and host before any network call. If the laptop uses mobile data or a guest Wi-Fi that isolates clients, the probe fails, so both devices must join the same ordinary Wi-Fi.

2. `check_reachable` calls `requests.get(url, stream=True, timeout=timeout, verify=verify_ssl)`. Requests resolves the host, opens a TCP connection to the phone on port 8080 and sends an HTTP GET for `/video`. The app replies with headers and one long response body made of JPEG images. `stream=True` stops Requests from downloading that endless body. `open_capture` then opens the same URL with OpenCV, and FFmpeg inside OpenCV decodes each JPEG into a BGR frame. `cap.read()` returns that frame. HTTP is the request-and-response protocol that carries the images.

3. A port selects a service on a device. IP Webcam serves its video on port 8080, so `CAMERA_URL` includes `:8080`. Without a port, the client uses the scheme default (80 for http, 443 for https). The phone has no service there, so the connection fails. `validate_url` returns the URL unchanged after its checks, so the port is preserved.

4. MJPEG over HTTP is a stream of complete JPEG images inside one long HTTP response; each image is a frame, so a loss does not corrupt the next one. RTSP is a dedicated streaming protocol with separate control and media channels, usually carrying H.264. This app uses the IP Webcam `/video` path over http or https, which is MJPEG. The URL scheme and `/video` path show this, the browser shows continuous video, and a `curl -s -D - -o /dev/null --max-time 3` request against the video address would show `Content-Type: multipart/x-mixed-replace`. `check_reachable` skips RTSP because Requests cannot test it.

5. The camera URL can carry a password, and a Git commit is public and permanent. Deleting a file later does not remove it from history, so anyone could read the address and watch the camera. The real value lives in `.env`, excluded by `.gitignore`; `.env.example` carries only `<phone-ip>`. `config.py` reads it with `load_dotenv()` and `os.getenv`. Console output and logs show only a masked line, never the URL. ADR-0001 records the rule.

### Part B: Python libraries

6. `cv2.VideoCapture` is the object that opens and reads the stream. `open_capture` builds it with `cv2.CAP_FFMPEG` and 5000 ms open and read timeouts, then checks `cap.isOpened()`. A false result makes it release the object and raise `CameraError`. In the loop, `cap.read()` returns `(ok, frame)`. When `ok` is false, `main.py` increments `failed_reads`; it continues below 10 and calls `reconnect` at 10. A good read resets the counter to zero.

7. A frame is a NumPy array with shape `(height, width, channels)`, so a 1280x720 colour frame has shape `(720, 1280, 3)`. Its type is `uint8`, with values 0 to 255. `resize_keep_aspect` uses `h, w = frame.shape[:2]` because height comes first. `Recorder.start` reads the same shape but stores `self.size = (w, h)`, since `VideoWriter` wants width first.

8. OpenCV stores colour as BGR. `imshow`, `imwrite` and `VideoWriter` all expect BGR, so the main path never converts and colours stay correct. A conversion is needed only for a library that expects RGB, such as PIL, matplotlib or some models; without it red and blue swap. The bonus detector uses `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`, the correct conversion for a grayscale image from an OpenCV frame.

9. `cv2.waitKey(1)` waits for a key and lets the window process events and redraw. Without it the window looks frozen. The code masks the result with `& 0xFF`. Esc is 27 and makes `handle_keys` return True to stop the loop. Other keys use `ord('s')`, `ord('r')` and `ord('m')`, and both cases are accepted. `reconnect` calls `cv2.waitKey(int(delay * 1000))` to keep the window responsive during the wait and to let Esc cancel a retry.

10. OpenCV fails slowly and vaguely on a bad address; `cap.read()` can hang instead of failing. `check_reachable` runs first and uses Requests with `stream=True` and the 5 second `REQUEST_TIMEOUT`. It flags 401 and 403 as login errors, calls `raise_for_status()`, and maps Timeout, ConnectionError and SSLError to clear `CameraError` messages. A bad address gives a one-line error and exit code 1 within the timeout. RTSP skips the probe because Requests cannot test it (ADR-0002).

### Part C: Video processing

11. `FpsMeter.tick` reads `time.perf_counter()` each call. After the first frame it computes `instant = 1.0 / (now - prev)`. The raw value jumps because network delivery and per-frame work vary. An exponential moving average smooths it: `fps = alpha * instant + (1 - alpha) * fps`, with alpha 0.1. The first frame leaves `fps` at 0.0. `draw_overlay` prints it with `FPS: {fps:4.1f}`.

12. Scale is target width divided by original width. For 1920x1080 to width 960, scale = 960 / 1920 = 0.5 and new height = 1080 * 0.5 = 540, so the result is 960x540. `resize_keep_aspect` computes `scale = target_width / w` and `new_h = int(h * scale) // 2 * 2`, which rounds down to an even height for video codecs. It calls `cv2.resize(frame, (target_width, new_h), interpolation=cv2.INTER_AREA)`, where the size is `(width, height)`. The unit test asserts that 1920x1080 becomes `(540, 960, 3)`.

13. `Recorder.start` gives `cv2.VideoWriter` the path from `timestamped_path`, a FourCC from `cv2.VideoWriter_fourcc(*'mp4v')`, the frame rate and the size `(w, h)`. The rate is `min(max(round(fps), 5), 30)`, or 15 when fps is zero, so it stays in a playable range. The size comes from the resized frame and every later `write` uses that frame size. A different size is silently dropped, and a wrong rate changes playback speed. `isOpened()` is checked; a false result clears the writer and raises `OSError`.

14. Drawing and encoding run on the CPU every frame and must finish inside the frame interval, about 33 ms at 30 FPS. `process_frame` draws the four overlays and writes the frame to the recorder, then copies the frame only when a recording, a message or motion boxes need extra drawing. That avoids a full `frame.copy()` on the common path. `resize_keep_aspect` reduces the frame to 960 pixels wide, and motion detection runs on that smaller frame. Labels are plain text. The writer rate is clamped, and the media folders can be moved to a faster disk.

15. `timestamped_path` in `recorder.py` creates the folder and builds a name from `datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]`. The slice keeps milliseconds, so two presses in one second still differ. A `while os.path.exists(path)` loop adds `_1`, `_2` and so on, so no file is overwritten. Screenshots use prefix `shot` and `.jpg`; recordings use `rec` and `.mp4`. The names sort in time order.

### Part D: Critical thinking

16. `MAX_FAILED_READS` is 10 in `main.py`. The loop continues on a single failed read and reconnects after 10 in a row. `reconnect` releases the old capture and tries `config.MAX_RECONNECTS` (5) times with `config.RECONNECT_DELAY` (2 seconds) between attempts. Each attempt calls `check_reachable` and `open_capture`; Esc cancels a wait. The last frame is shown with a "Reconnecting..." label. After the last attempt it raises `CameraError`, which the outer handler turns into a one-line error and exit code 1. Ten reads plus 5 attempts at 2 seconds give roughly 10 to 15 seconds of patience: long enough for a Wi-Fi blip, short enough to avoid a frozen window (ADR-0003).

17. Releasing frees the network connection and the camera, so the IP Webcam app has no stuck client and another client can connect. `VideoWriter.release()` also finalises the MP4 by writing its headers and index; a recording left open can be unplayable or truncated. The `finally` block in `main.py` calls `recorder.stop()` first, then `cap.release()`, then `cv2.destroyAllWindows()`. It runs on Esc, Ctrl+C, window close and errors. TC09 and TC10 are the checks that a file saved on exit still plays.

18. Record only places and people who agreed, and use a camera you own or have permission to use. Files stay local in `screenshots/` and `recordings/`, both ignored by Git; the viewer uploads nothing. The red REC badge and elapsed seconds make recording visible. Keep the address out of logs and evidence, and delete recordings you no longer need. Kenya's Data Protection Act covers personal data, and video of identifiable people can be personal data, so consent, limited retention and secure storage apply. The responsible-use note above and the masked console line are part of that design.

19. One loop would block on `cap.read()` for a slow camera and stall the other nine. Decoding, resizing and drawing ten streams would also exceed the CPU budget and the Wi-Fi bandwidth. The redesign gives each camera its own reader thread or process with its own capture and reconnect logic. Each reader puts only its latest frame on a small queue. A display thread tiles ten low-resolution frames and drops stale ones instead of blocking. Decode on the GPU where available, or move processing to a server. Reusing one detector across cameras extends the bonus idea.

20. Hardest bug. The code contains traps that suit this answer: a 0-byte recording when the frame size passed to `VideoWriter` differs from the declared size (`Recorder.start` sets `self.size = (w, h)` and checks `isOpened()`), a window that freezes without `waitKey`, a hang on a wrong IP before the Requests probe, and a Qt xcb error on Wayland. Name one real bug, say how you found the cause through prints, documentation or the smallest failing case, and say what you would do differently, such as testing failure paths earlier, writing the retry logic first or logging from the start.

[PERSONAL NOTE TO ADD BY THE STUDENT: one short paragraph on the real bug you met, how you found it, and what you would change. Do not present an example above as your own experience.]

## Bonus description

The bonus adds motion detection and auto-record through one path (ADR-0007). `MotionDetector` converts the resized frame to grayscale with `COLOR_BGR2GRAY`, blurs it with a 21x21 Gaussian kernel, takes `cv2.absdiff` against the previous frame, thresholds at 25, dilates twice, and returns contours whose area is at least `min_area` (800 in `main.py`). The `M` key toggles detection. Green rectangles mark the boxes. Three consecutive frames with motion start `Recorder`, and recording stops about 5 seconds after the last motion. `MOTION_MIN_AREA`, `MOTION_FRAMES_TO_START` (3) and `MOTION_STOP_AFTER` (5.0 seconds) are constants at the top of `main.py`. Auto-record never stops a recording the user started with `R`, because `state.manual_recording` takes priority.

## Conclusion

The program meets the core brief: a live stream with four overlays, screenshot and recording keys, a reachability probe, bounded reconnects and safe cleanup. Nine unit tests pass. The two tests that need no camera ran and passed; the eight GUI tests need a phone session and are documented as Not run. The next improvements are a threaded writer so disk delays cannot stall the display, a multi-camera layout built from per-camera reader threads, and an option to import the phone certificate instead of disabling TLS verification.

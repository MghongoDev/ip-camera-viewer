# IP Camera Viewer

A desktop viewer for a camera you own. It reads an MJPEG stream from an Android phone running IP Webcam over your local Wi-Fi and shows it in an OpenCV window. Every frame carries four overlays: a timestamp, a camera name, the resolution and an estimated FPS. The S key saves a screenshot, R starts and stops an MP4 recording, and M toggles motion detection with auto-record. Esc quits and releases everything.

Use only a camera you own or have permission to use. Record only people and places that have agreed. Media stays on your machine. The viewer never uploads it.

## Requirements

- Python 3.12 or newer. The pinned numpy needs 3.12. The source itself runs on 3.10 with older package pins.
- An Android phone with the IP Webcam app.
- The phone and the computer on the same Wi-Fi network.
- The pinned packages listed in `requirements.txt`.

## Install

Clone the repository, then create a virtual environment and install the packages.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate` instead.

The pinned versions are opencv-python 5.1.0.95, numpy 2.5.5, requests 2.34.2 and python-dotenv 1.2.4. Install `opencv-python`, not `opencv-python-headless`. The headless build has no window to show video.

## Set the camera URL

The real address lives in `.env`, which Git ignores. Never commit it.

1. Copy the template: `cp .env.example .env`.
2. Start IP Webcam on the phone and tap **Start server**.
3. Read the HTTPS address the app shows. Add `/video` to the path.
4. Set `CAMERA_URL` in `.env` to `https://<phone-ip>:8080/video`. Replace `<phone-ip>` with the address the app showed.
5. Set `CAMERA_NAME` to the label you want on screen.

IP Webcam serves HTTPS with a certificate it signs itself. Keep `CAMERA_VERIFY_SSL=false`. The viewer then accepts the certificate for both the requests probe and FFmpeg. This is a trade-off for a network you trust. Someone on that network could pretend to be the camera. If you install the phone certificate on the computer, set the value to `true` to restore verification.

Every setting has a default. Edit only the ones you need to change. The viewer reads `.env` when it starts. A variable set in the shell takes precedence over the file.

## Run

```bash
python main.py
```

A window opens with live video. Press Esc to quit. Any active recording is finalised and the camera is released.

## Controls

| Key | Action |
| --- | --- |
| S | Save the current frame as a JPEG in `screenshots/`. |
| R | Start a recording, or stop the active one. Files go in `recordings/`. |
| M | Toggle motion detection. Motion can start a recording and stop it about five seconds after the last movement. |
| Esc | Quit. The viewer finalises any active recording and releases the camera. |

Ctrl+C in the terminal and the window close button also shut the viewer down cleanly.

## File map

| File | Purpose |
| --- | --- |
| `main.py` | The main loop, key handling and safe shutdown. |
| `config.py` | Reads settings from `.env` and the environment. |
| `camera.py` | Validates the address, probes reachability and opens the capture. |
| `overlay.py` | Resizes frames and draws the overlays and FPS meter. |
| `recorder.py` | Writes screenshots and MP4 recordings. |
| `motion.py` | Finds changed regions for motion detection. |
| `requirements.txt` | Pinned package versions. |
| `.env.example` | Template for settings. Safe to commit. |
| `.env` | Your real settings. Never commit. |
| `tests/test_units.py` | Unit tests for the pure helpers. |
| `docs/` | Tutorials, how-to guides, the glossary and architecture decision records. |

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| The phone cannot be reached | Both devices on the same Wi-Fi. Not mobile data. Not a guest network with client isolation. VPN off on the computer. Firewall allows the connection. The app is running and the screen is on. |
| The stream will not open | The path ends in `/video`. Re-read the address in the app. The phone IP may have changed. |
| A certificate error appears | Keep `CAMERA_VERIFY_SSL=false`. IP Webcam signs its own certificate. |
| The window will not open, or Qt reports an xcb plugin error | On Wayland, run `export QT_QPA_PLATFORM=xcb` before `python main.py`. Install the system libraries the error names. |
| `cv2.imshow` is unavailable | Install `opencv-python`, not `opencv-python-headless`. The headless build has no window. |
| A recording is empty or will not play | Check the file size in `recordings/` and play the file in a local player. |

## Documentation

The documentation follows the Divio four-part model. Each part answers a different question.

| Part | Question | Where to start |
| --- | --- | --- |
| Tutorial | I want to learn the viewer | [Getting started](docs/tutorials/getting-started.md) |
| How-to | I want to do a task | [Configure the camera](docs/how-to/configure-the-camera.md), [Capture media](docs/how-to/capture-media.md), [Recover from a dropped stream](docs/how-to/recover-from-a-dropped-stream.md) |
| Reference | I want the facts | [Configuration](docs/reference/configuration.md), [controls](docs/reference/controls.md), [module map](docs/reference/module-map.md), [test cases](docs/reference/test-cases.md) and [GLOSSARY.md](GLOSSARY.md) |
| Explanation | I want to know why | [Architecture](docs/explanation/architecture.md), [video pipeline](docs/explanation/video-pipeline.md), [security and privacy](docs/explanation/security-and-privacy.md) and the [ADRs](docs/adr/0001-keep-camera-secrets-out-of-git.md) |

The glossary defines every term with a special meaning. The ADRs in `docs/adr/` record the choices that are not obvious from the code.

## Status

The viewer is feature complete for its scope. It shows live video with four overlays, saves screenshots and recordings, detects motion and reconnects after a short drop. The nine unit tests pass with `python -m unittest discover -s tests`. Two failure paths were checked. An invalid address and an unreachable address each print a one-line error and exit with code 1. Live GUI tests were not run in this environment, so the on-screen behaviour has not been verified here.

The supplied implementation guide is assignment source material. It is deliberately untracked. The `.gitignore` file excludes it so its sample values never enter the repository. The documentation describes the shipped code.

# Getting started

In this tutorial you bring up IP Webcam on a phone and watch its video in the viewer. By the end you will see a live window with four overlays. You will save a screenshot and quit cleanly.

## Learning goals

- Connect a phone camera to the viewer over your Wi-Fi.
- Read the address the app shows and put it in the right place.
- Recognise the four overlays on the frame.
- Save a screenshot and shut the viewer down safely.

## Prerequisites

- Python 3.12 or newer. The pinned numpy needs 3.12. The source runs on 3.10 with older pins.
- An Android phone with the IP Webcam app.
- The phone and the computer on the same Wi-Fi. Not mobile data and not a guest network.
- Basic use of a terminal.

## Step 1: Get the stream running in a browser

Install IP Webcam on the phone and open it. Tap **Start server**. The app shows an HTTPS address. Note it. Add `/video` to the path to get the video stream.

On the computer, open that address in a browser. You should see live video from the phone. Do this before writing any code. If the browser cannot show the stream, fix the network first. Check that both devices share the same Wi-Fi, that the phone is not on mobile data, and that no VPN or guest-network isolation is in the way.

## Step 2: Install the viewer

Clone the repository and install the pinned packages in a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows users activate with `.venv\Scripts\activate`.

## Step 3: Tell the viewer where the camera is

Copy the settings template and open it.

```bash
cp .env.example .env
```

Set `CAMERA_URL` to `https://<phone-ip>:8080/video`. Replace `<phone-ip>` with the address the app showed. Set `CAMERA_NAME` to the label you want on screen. Keep `CAMERA_VERIFY_SSL=false` because the phone signs its own certificate.

The `.env` file stays on your machine. Git ignores it.

## Step 4: Run the viewer

```bash
python main.py
```

A window opens with live video. Each frame carries four overlays. The timestamp at the top left updates once a second. Below it is the camera name. The bottom left shows the resolution as width by height. The last line shows the estimated FPS. The frame is resized to a fixed width, and circles stay round.

## Step 5: Save a screenshot and quit

Press S. A confirmation appears on screen and a JPEG lands in `screenshots/`. Press Esc to close the window. The terminal returns without a traceback. If a recording had been running, the viewer would finalise it before closing.

Ctrl+C in the terminal and the window close button also shut the viewer down safely.

## What you learned

You connected a phone camera, configured the address in `.env`, read the overlays, saved a frame and quit cleanly.

## Next steps

- [Configure the camera](../how-to/configure-the-camera.md) to change timeouts, the display width and the reconnect settings.
- [Capture media](../how-to/capture-media.md) to record video and use motion detection.
- [Recover from a dropped stream](../how-to/recover-from-a-dropped-stream.md) to understand retries.

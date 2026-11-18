# Configure the camera

This guide sets the camera address and the viewer's runtime settings. Do this before the first run, or whenever the phone address changes.

## Set the address

1. Copy the template: `cp .env.example .env`.
2. Start IP Webcam on the phone and tap **Start server**.
3. Set `CAMERA_URL` in `.env` to `https://<phone-ip>:8080/video`. Use the address the app shows in place of `<phone-ip>`. Keep the `/video` path.
4. Set `CAMERA_NAME` to the label shown on screen.
5. Run `python main.py`.

The viewer validates the address when it starts. An empty value, a wrong scheme or a missing host stops the program with a one-line error and exit code 1. An address that parses but does not answer fails at the reachability probe with a timeout message and exit code 1. An RTSP address is accepted, but it skips the reachability probe because Requests cannot test it.

## Settings

Every setting has a default, so leave unchanged lines as they are. `config.py` reads `.env` at startup. A variable set in the shell takes precedence over the file.

| Setting | Default | What it does |
| --- | --- | --- |
| `CAMERA_URL` | empty | The full HTTPS address of the video stream. Required. |
| `CAMERA_NAME` | `Camera 1` | Text drawn on the frame. |
| `DISPLAY_WIDTH` | `960` | Width in pixels. Height is scaled to keep the aspect ratio and rounded to an even number. |
| `MAX_RECONNECTS` | `5` | Number of times to reopen the stream after a dead connection. |
| `RECONNECT_DELAY` | `2` | Seconds waited on each reconnect attempt. |
| `REQUEST_TIMEOUT` | `5` | Seconds allowed for the reachability probe before it gives up. |
| `CAMERA_VERIFY_SSL` | `false` | Whether Requests and FFmpeg verify the camera's TLS certificate. |

## Handle the self-signed certificate

IP Webcam serves HTTPS with a certificate it signs itself. With `CAMERA_VERIFY_SSL=false`, the reachability probe skips verification and suppresses the warning, and FFmpeg sets `tls_verify;0` before opening the HTTPS stream. The viewer can then use the address the app shows without importing a certificate.

This is a trade-off for a network you trust. Someone on the same network could impersonate the camera. If you install the phone certificate on the computer, set `CAMERA_VERIFY_SSL=true` to restore verification. The probe then checks the certificate and reports an SSL error if it is not trusted.

## Keep the address secret

`.env` is gitignored. Never paste the real address into a tracked file, a screenshot or a log message. The viewer prints a masked notice at startup and never prints the URL. The `.env.example` file holds placeholders only and is safe to commit.

## Related

- [Getting started](../tutorials/getting-started.md)
- [Recover from a dropped stream](recover-from-a-dropped-stream.md)

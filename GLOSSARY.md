# Glossary

This file defines the words the project uses. Documentation uses these words in this sense.

**ADR.** Architecture decision record. A short note that records a choice, the reason for it, and what follows from it. ADRs live in `docs/adr/`.

**aspect ratio.** The width-to-height ratio of a frame. Resizing keeps this ratio so circles stay round.

**BGR.** The colour order OpenCV uses: blue, green, red. Image libraries such as PIL use RGB. A frame passed between them needs a conversion.

**camera URL.** The address of the video stream, stored as `CAMERA_URL` in `.env`. It includes the phone address, port and the `/video` path. It never appears in tracked files.

**capture.** The `cv2.VideoCapture` object that reads frames from the stream. Releasing it frees the camera for the next client.

**Divio four-part structure.** A way to organise documentation into tutorials, how-to guides, reference and explanation. Each part answers a different question.

**failed read.** One call to `cap.read()` that returns no frame. A short run of failed reads is tolerated before the viewer reconnects.

**FourCC.** A four-character code that names a video codec. The recorder uses `mp4v`.

**frame.** One image in the video stream. In code it is a NumPy array with shape `(height, width, channels)` and type `uint8`.

**FPS.** Frames per second. The viewer estimates it from the time between frames and smooths the result.

**IP Webcam.** The Android app on the phone. It serves an MJPEG stream over HTTP or HTTPS on the local network.

**MJPEG.** Motion JPEG. A sequence of JPEG images sent over one long HTTP response.

**overlay.** Text or shape drawn onto a frame before display. The viewer draws timestamp, camera name, resolution, FPS, a REC badge and status messages.

**reachability probe.** A short `requests.get` call with `stream=True` and a timeout. It fails fast before OpenCV tries to open an address that may hang.

**reconnect.** The bounded retry that follows a dead stream. It releases the old capture and opens a new one up to `MAX_RECONNECTS` times.

**REC badge.** The red dot and elapsed time drawn on screen while a recording runs.

**recording.** An MP4 file written through `cv2.VideoWriter`. `R` starts and stops it; motion can start and stop it too.

**self-signed certificate.** A TLS certificate the phone issues for itself. Requests and FFmpeg reject it by default. `CAMERA_VERIFY_SSL=false` tells both to accept it on this trusted local network.

**screenshot.** A JPEG written by `S` from the last good frame. Its name includes a millisecond timestamp.

**TC.** Test case. `TC01` to `TC10` are the ten integration tests in the implementation guide.

**test evidence.** The screenshot and written record attached to a test case. Evidence must hide the camera address and any credentials.

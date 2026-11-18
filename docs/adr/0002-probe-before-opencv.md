# 0002 Probe the address before opening OpenCV

Status: Accepted

## Context

`cv2.VideoCapture` can block for a long time on a wrong address or a dropped connection. A wrong IP on the local subnet is the worst case: the call hangs instead of failing.

## Decision

Call `check_reachable` first. It uses `requests.get` with `stream=True`, a short timeout and status checks. Only then does `open_capture` touch the address.

## Consequences

Bad addresses produce a clear message within `REQUEST_TIMEOUT` seconds. The probe downloads only the start of the MJPEG stream. RTSP addresses skip the probe because Requests cannot test them.

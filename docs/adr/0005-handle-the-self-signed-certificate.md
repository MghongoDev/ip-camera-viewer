# 0005 Handle the self-signed camera certificate

Status: Accepted

## Context

The phone serves HTTPS with a certificate it signs itself. Requests rejects it as an SSL error and FFmpeg rejects it as a certificate verification failure. The viewer must still connect to the address the camera shows.

## Decision

Add `CAMERA_VERIFY_SSL`, default `false`. When it is false, Requests skips verification with warnings suppressed, and `open_capture` sets `OPENCV_FFMPEG_CAPTURE_OPTIONS=tls_verify;0` before opening an HTTPS stream. The option is documented as a trusted-local-network trade-off.

## Consequences

The viewer connects to the HTTPS address from the app without importing a certificate. Anyone with local network access could impersonate the camera. Users who import the phone certificate can set the value to `true` and get verification back.

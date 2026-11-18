# Recover from a dropped stream

This guide explains what the viewer does when frames stop arriving and how to test it.

## What happens on a dropped stream

The viewer counts consecutive failed reads. A single dropped frame is normal on Wi-Fi. Ten failed reads in a row mark the connection as dead. Below that limit the viewer keeps the last frame on screen and waits for the next one. Any good read resets the counter.

At ten failures the viewer shows "Reconnecting..." on the last frame. It releases the old capture and tries to reopen the stream. It makes at most five attempts with a two-second wait before each one. Each attempt probes the address with Requests before OpenCV opens it. The progress prints go to the terminal. Press Esc during a wait to cancel and quit.

If an attempt succeeds, the counter resets and video resumes. If all five attempts fail, the viewer prints one clear error and exits with code 1. The wait is bounded and the window shows what is happening.

## Test a drop

1. Start the viewer with a good connection.
2. Turn off the phone's Wi-Fi for about ten seconds, then turn it back on.
3. Watch for a short interruption. The viewer either resumes on its own or reports that it could not reconnect after five attempts.
4. To see the clean failure path, leave the Wi-Fi off until the attempts run out.

Do not point the viewer at a dead address to test this. A bad address fails earlier, at the reachability probe, before the loop starts.

## Other clean failures

- An address that is empty or has a wrong scheme stops at validation with a one-line error and exit code 1.
- An address that parses but does not answer stops at the probe with "The camera did not answer in time. Is the app running on the same Wi-Fi?" and exit code 1.
- An address that returns 401 or 403 reports that the camera rejected the login.
- An HTTPS address with an untrusted certificate reports a self-signed certificate error. Set `CAMERA_VERIFY_SSL=false` on a trusted local network.

## Safe shutdown

Every exit path runs the same cleanup. The viewer stops any active recording, releases the capture and closes the window. Esc, Ctrl+C and the window close button all follow this path. A recording started before a drop is finalised before reconnecting, so it stays playable. An unexpected error is written to `app.log`, and the user sees a one-line message instead of a traceback.

## Related

- [Configure the camera](configure-the-camera.md)
- [Capture media](capture-media.md)

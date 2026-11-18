# Controls

The viewer uses the keyboard and the window close button. There are no on-screen buttons. `cv2.waitKey(1)` runs once per frame, so a key press is read within one frame interval. During reconnect the wait is longer: `waitKey(RECONNECT_DELAY * 1000)`, where `RECONNECT_DELAY` is 2 seconds by default. See [configuration.md](configuration.md) for the values.

## Keys and window actions

| Input | Action | Effect on screen and files |
|---|---|---|
| `Esc` | Stop the loop. | If a recording is active, `Recorder.stop()` finalizes it first. The `finally` block releases the capture and closes windows. Exit code 0. |
| `S` or `s` | Save a screenshot. | Writes `screenshots/shot_{milliseconds}.jpg` from the current frame. The frame carries the four overlays but no REC badge or status text. A confirmation shows for 2 seconds. An `OSError` shows its message instead. |
| `R` or `r` | Toggle recording. | When idle, starts `recordings/rec_{milliseconds}.mp4`. When active, stops it and shows `Recording saved`. An `OSError` shows its message instead. |
| `M` or `m` | Toggle motion detection. | Clears drawn boxes and shows `Motion on` or `Motion off` for 2 seconds. Detection then starts or stops on the next frame. |
| `Ctrl+C` | Interrupt from the terminal. | Prints `Interrupted, shutting down.` The `finally` block still stops the writer and releases the capture. Exit code 0. |
| Window close (X) | Close the OpenCV window. | `getWindowProperty(WINDOW, WND_PROP_VISIBLE) < 1` breaks the loop. Resources are released. Exit code 0. |

## Recording details

`Recorder.start` takes the frame size from the resized frame, so every written frame matches the declared size. The codec FourCC is `mp4v`. The rate is `round(fps)` clamped to 5 through 30, or 15 when `fps` is zero. A recording that cannot open raises `OSError` and the message appears on screen.

While a writer is active, `process_frame` draws a red circle at the top right and the text `REC {elapsed}s` next to it. Both manual and motion recordings show this badge. A status message, when present, appears at `(10, 80)` for `MESSAGE_SECONDS` seconds.

## Motion key behaviour

`M` only toggles detection. Auto-record uses the same `Recorder` as `R`. A manual recording has priority: motion never stops a recording started with `R`. When motion starts a recording, it stops about 5 seconds after the last frame with motion. Green rectangles mark the changed regions while detection is on.

## Cancel a reconnect wait

When the stream drops, the window shows `Reconnecting...` and the program tries to open a new capture up to `MAX_RECONNECTS` times. Each attempt waits `RECONNECT_DELAY` seconds. Pressing `Esc` during that wait raises `KeyboardInterrupt`, so the program shuts down through the same `finally` block.

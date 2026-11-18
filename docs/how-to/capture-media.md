# Capture media

This guide saves stills and video from the live window and sets up recording on motion.

## Save a screenshot

1. Start the viewer with `python main.py`.
2. Press S while the camera is showing.
3. Look for the confirmation on screen. The JPEG is in `screenshots/` in the project folder.

The file name has a millisecond timestamp. Two presses in the same second produce two separate files. The viewer adds a numeric suffix if a name already exists, so nothing is overwritten. The screenshot is the displayed frame with the four overlays. It does not include the REC badge or a status message.

## Record video

1. Press R. A red dot and a timer appear at the top right. The timer counts whole seconds.
2. Press R again to stop. The confirmation says the recording was saved.
3. Open the MP4 from `recordings/` in a local player. Check its length and that it plays at normal speed.

The recorder writes MP4 with the `mp4v` codec. It sizes the file to the displayed frame. It clamps the frame rate to a value between 5 and 30, or uses 15 when no estimate is available. The file contains the four overlays. It does not contain the REC badge or status messages. Files are named with a millisecond timestamp and never overwrite each other.

`recordings/` and `screenshots/` are gitignored. Media stays on your machine.

## Record on motion

1. Press M to toggle motion detection. A "Motion on" message appears.
2. Comparison happens on the resized frame, so it stays fast. Changed regions are drawn as green rectangles.
3. Motion on three consecutive frames starts the recorder. The message says motion started the recording.
4. The recording stops about five seconds after the last motion. The message says the motion recording was saved.

Press M again to turn detection off. A recording you started with R has priority. Motion logic never stops a manual recording. Motion detection uses the same recorder as the R key, so capture behaviour is identical.

## Related

- [Getting started](../tutorials/getting-started.md)
- [Configure the camera](configure-the-camera.md)

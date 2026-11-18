# 0004 Write media before drawing status

Status: Accepted

## Context

A recording and a screenshot should carry the timestamp and camera name but not the REC badge or a status message. Copying every frame to keep a clean version costs time on each frame.

## Decision

Draw the overlays, write the frame to the recording, then draw the REC badge and message on a copy made only when a badge or message is present. Screenshots come from the unbadged frame.

## Consequences

The common frame path makes no copy. Saved media contains the four overlays and no status decoration. The code stays easy to read because one function handles the drawing order.

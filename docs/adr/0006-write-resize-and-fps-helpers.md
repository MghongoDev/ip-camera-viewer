# 0006 Write the resize and FPS helpers locally

Status: Accepted

## Context

The brief asks for the resize calculation and the FPS estimate in the report. A library call hides both calculations from the code a marker reads.

## Decision

Implement `resize_keep_aspect` and `FpsMeter` in `overlay.py` with NumPy and `time.perf_counter`. Do not depend on `imutils`.

## Consequences

The code shows the scale factor, the even-height rounding and the moving average. Two technical questions can be answered by pointing at the functions. One less package needs pinning.

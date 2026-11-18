# 0007 Share one path for the two bonus items

Status: Accepted

## Context

The brief offers bonus marks for motion detection and for auto-record on motion. Building them separately duplicates the frame loop and the writer.

## Decision

One `MotionDetector` finds changed regions on the resized frame. The main loop starts and stops the existing `Recorder` when motion crosses a threshold. A manual recording has priority and is never stopped by motion logic.

## Consequences

Two bonus items come from one code path. The `M` key toggles detection. Auto-record stops about five seconds after the last motion.

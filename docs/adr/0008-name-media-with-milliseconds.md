# 0008 Name media with milliseconds

Status: Accepted

## Context

Two key presses in one second produce the same second-level name. Overwriting a file loses evidence.

## Decision

`timestamped_path` builds a name with a millisecond timestamp and adds a numeric suffix while the path exists. The folder is created on demand.

## Consequences

Two screenshots taken quickly stay separate. No file is overwritten. The names sort in time order.

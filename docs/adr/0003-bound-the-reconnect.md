# 0003 Bound the reconnect loop

Status: Accepted

## Context

A dropped Wi-Fi link can fail one read and recover on the next. A dead camera will fail every read forever. An unbounded retry leaves the user staring at a frozen window.

## Decision

Tolerate `MAX_FAILED_READS` consecutive failed reads, then reconnect at most `MAX_RECONNECTS` times with `RECONNECT_DELAY` seconds between attempts. Any good read resets the counter. Esc cancels a wait.

## Consequences

Ten failed reads and five attempts at two seconds give roughly ten to fifteen seconds of patience. A brief glitch passes unnoticed. A dead camera produces one clear error and exit code 1.

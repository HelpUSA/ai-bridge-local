
# AI Bridge Local - Remove worker running notice report 2026-06-15

## Status
Implemented for release 0.5.6.

## Reason
The 0.5.5 patch changed the running notice text but did not fully stop the worker from sending it.

## Result
Expected flow: one queued notice plus one final result.

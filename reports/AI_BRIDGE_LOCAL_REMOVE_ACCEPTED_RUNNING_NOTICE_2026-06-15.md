
# AI Bridge Local - Remove accepted running notice report 2026-06-15

## Status
Implemented for release 0.5.9.

## Reason
The previous patch removed the worker_running_notice_disabled text, but format_accepted_message still emitted [AI_LOCAL] status=running.

## Result
enqueue_accepted_message is now a no-op and calls were removed from run-command paths.

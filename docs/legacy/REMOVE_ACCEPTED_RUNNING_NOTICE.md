
# AI Bridge Local - Remove accepted running notice 0.5.9

## Objective
Remove the worker-side accepted/running notice completely.

## Behavior
Expected watcher flow:

1. Gateway sends the queued notice.
2. Worker executes the command.
3. Worker sends only final AI_LOCAL_RUN.

No worker message with status=running should be sent.

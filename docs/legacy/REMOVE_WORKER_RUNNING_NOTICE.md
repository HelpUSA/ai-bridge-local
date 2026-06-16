
# AI Bridge Local - Remove worker running notice 0.5.6

## Objective
Remove the intermediate worker running message completely.

## Behavior
- Gateway sends the single queued notice.
- Worker sends only the final AI_LOCAL_RUN/AI_LOCAL_ERRO result.
- No worker running/silent notice should be injected into the ChatGPT composer.

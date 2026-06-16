
# AI Bridge Local - Disable worker running notice 0.5.5

## Objective
Prevent intermediate worker progress notices from occupying the ChatGPT composer.

## Behavior
- Gateway still sends one queued notice.
- Worker no longer sends running/silent progress notices.
- Final AI_LOCAL_RUN remains unchanged.

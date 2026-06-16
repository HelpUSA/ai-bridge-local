
# AI Bridge Local - Immediate gateway feedback 0.5.2

## Objective
Every command submission must produce fast visible feedback.

## Behavior
- Valid run-command envelopes enqueue an immediate source-chat message with status=queued and no_reply=1.
- Invalid but parseable envelopes enqueue an immediate AI_LOCAL_ERRO message to the source chat.
- Nothing is executed when validation fails.


# AI Bridge Local - Gateway feedback dedup 0.5.3

## Objective
Keep the useful fast feedback from 0.5.2 without flooding chats.

## Behavior
- Gateway feedback command_id is deterministic per original command and source chat.
- Duplicate submissions do not create duplicate queued notices.
- The old intermediate worker running notice is silenced when present.
- The final AI_LOCAL_RUN result remains unchanged.
- next-action uses an atomic queued-to-delivering claim when the known line is present.

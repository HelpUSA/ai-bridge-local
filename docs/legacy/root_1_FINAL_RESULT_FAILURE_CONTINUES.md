
# AI Bridge Local - Final result failure continues 0.5.10

## Objective
Prevent chats from stopping after a failed command.

## Behavior
Final AI_LOCAL_RUN always includes:

- result_is_final=1
- chat_can_continue=1

Success:

- success=1
- next_action=continue_next_activity

Failure:

- success=0
- next_action=fix_error_before_continue

The chat should continue by analyzing the failure and proposing a safe correction.


# AI Bridge Local - Final result continue hint 0.5.7

## Objective
Add explicit continuation guidance to the final worker result message.

## Behavior
Successful final result includes:
- result_is_final=1
- chat_can_continue=1
- next_action=continue_next_activity

Failed final result includes:
- result_is_final=1
- chat_can_continue=0
- next_action=fix_error_before_continue

No additional intermediate chat message is sent.

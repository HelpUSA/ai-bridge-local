# Command accepted progress notice

Commands do not need to be split into smaller commands.

Current contract:
- The gateway may emit an initial queued acknowledgement.
- The worker must not emit an intermediate running notice as the authoritative result.
- The final [AI_LOCAL_RUN] result remains the authoritative execution result.
- A final result can include chat_can_continue and next_action so the chat can continue safely.

Historical note: older releases used a command accepted/running progress notice. Later releases removed that intermediate worker running notice and kept the flow as queued initial feedback plus final AI_LOCAL_RUN.

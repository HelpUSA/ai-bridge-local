# Command status probe

scripts/watcher/command_status_probe.py inspects local AI Bridge command state by command_id in queue_local.db.

Purpose:
- confirm whether a command is queued, delivering, acked, or failed;
- reduce repeated commands when an AI_LOCAL_RUN result was produced but not visible in chat;
- support safe follow-up after result_is_final=1, chat_can_continue=1, and next_action are present in final results.

Operational rule:
- use the probe before repeating a command that may already have run;
- do not treat queued local status messages as proof that the original run-command is still pending;
- prefer longer local script_text scripts for multi-step work to reduce envelope parsing errors.

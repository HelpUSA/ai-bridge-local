# AI Bridge Local - Command accepted progress notice 0.4.99

## Objective
Avoid the impression that long commands are stuck while keeping large watcher commands allowed.

## New behavior
When the worker receives a run-command action, it immediately queues a short message back to the source chat before starting the local subprocess.

Expected message:

[AI_LOCAL]
comando aceito, execucao iniciada
id=<command_id>
status=running
no_reply=1
cwd=<cwd>

## Implementation
- brain_worker.py
- format_accepted_message(action)
- enqueue_accepted_message(action)
- enqueue_accepted_message(action) is called immediately before execute_command(payload, command_id)

## Compatibility
The final [AI_LOCAL_RUN] result remains unchanged.
The final ack remains unchanged.
Commands do not need to be split into smaller commands.

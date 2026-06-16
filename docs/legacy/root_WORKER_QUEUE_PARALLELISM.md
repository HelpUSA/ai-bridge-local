# AI Bridge Local - Worker queue parallelism 0.5.0

## Objective
Allow several chats to send commands without forcing the worker to execute every source strictly one by one.

## Design
The gateway continues to store pending actions in queue_local.db.
The worker now submits run-command actions to a bounded ThreadPoolExecutor.
The default parallelism is three workers and can be changed with AI_BRIDGE_MAX_PARALLEL_RUN_COMMANDS.

## Safety
Commands sharing the same cwd are serialized with a cwd lock.
Commands from different cwd values can run in parallel.
The accepted notice from 0.4.99 is preserved.
The final [AI_LOCAL_RUN] result and final ACK are preserved.

## Notes
This is intentionally conservative.
Git commit, push, migration, and write operations in the same repository should still be serialized by cwd.

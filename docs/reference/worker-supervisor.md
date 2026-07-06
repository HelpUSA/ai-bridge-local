---
type: reference
status: draft
tags:
 - worker
 - supervisor
 - heartbeat
---

# Worker supervisor

The worker supervisor owns worker liveness and safe recovery.

## 0.5.79 conservative stale PID hotfix

If temp/brain_worker.pid exists:

1. Read the PID.
2. Check whether the process exists.
3. If the process does not exist, rename the PID file to a stale backup.
4. Start a new worker.
5. If there is any doubt, mark needs_supervisor or needs_user.

The hotfix must not kill a process solely because a PID file exists.

## Full supervisor target

Each worker instance records:

- worker_instance_id
- pid
- process_start_time
- started_at
- last_heartbeat_at
- current_command_id
- status
- command_hash

The supervisor validates PID and process start time before considering a worker alive.

## Heartbeat

Workers emit heartbeat while idle and while running commands. Heartbeat loss transitions the worker to stale and triggers recovery policy.

## Recovery rules

- Remove stale PID files only when the PID does not exist.
- Kill a process tree only after strong validation of command line, start time, worker instance and parent process.
- Prefer needs_supervisor over unsafe kill.
- Persist every recovery decision.

## Bridge Doctor

Bridge Doctor should expose at minimum:

- gateway status
- worker count
- last worker heartbeat
- stale PID detection
- commands by state
- browser actions pending
- dead letters

This diagnostic can start as CLI or JSON endpoint before the full Control Center v2.

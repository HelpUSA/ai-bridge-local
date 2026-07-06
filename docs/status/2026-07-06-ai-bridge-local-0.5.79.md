# AI Bridge Local 0.5.79 - Conservative stale worker PID recovery

Date: 2026-07-06

## Summary

Version 0.5.79 implements the first code change from the control plane roadmap: conservative recovery for stale `temp/brain_worker.pid` files.

## Behavior

When `brain_worker.py` starts and finds a PID file:

- If the PID belongs to a running process, the worker still exits without killing anything.
- If the PID is not running or is invalid, the PID file is renamed to a timestamped backup instead of being deleted.
- If the backup fails, the worker writes `temp/brain_worker.needs_supervisor` and exits with failure.

## Safety boundary

This version does not kill processes. Full worker identity validation using `worker_instance_id`, process start time and heartbeat remains scheduled for the worker supervisor milestone.

## Validation

- `python -m py_compile brain_worker.py scripts/watcher/smoke_stale_worker_pid_0579.py`
- `python scripts/watcher/smoke_stale_worker_pid_0579.py`
- `git diff --check`

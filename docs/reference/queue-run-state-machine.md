---
type: reference
status: draft
tags:
 - queue
 - runs
 - state-machine
---

# Queue and run state machine

Durable Queue v2 separates command intent, execution runs and browser delivery.

## Command states

- created
- validated
- queued
- leased
- running
- succeeded
- failed
- timed_out
- cancelled
- dead_letter

## Valid command transitions

- created -> validated -> queued -> leased -> running -> succeeded
- created -> validated -> queued -> leased -> running -> failed
- queued -> lease_expired -> retry_scheduled -> queued
- running -> timed_out -> retry_scheduled
- running -> timed_out -> dead_letter
- failed -> retry_scheduled
- failed -> needs_chat
- failed -> dead_letter

## Lease rules

A worker claims a command by creating a lease with lease_expires_at. A command is not acknowledged when it is merely leased. Ack is recorded only after the final result is persisted.

If a worker dies, the lease expires and the control plane decides retry, needs attention or dead letter. Retries require max attempts and cooldown.

## Run states

A command can have multiple runs.

- created
- started
- heartbeat
- complete
- failed
- timed_out
- abandoned

Each run records run_id, command_id, trace_id, worker_instance_id, started_at, last_heartbeat_at, finished_at, return_code, stdout_log_path, stderr_log_path, summary, error_class and next_action.

## Browser action states

Browser delivery is separate from command execution.

- requested
- delivered_to_extension
- sent_to_chat
- failed
- unavailable
- expired
- deduped

This prevents the control plane from confusing local command success with successful chat delivery.

## QueueAdapter minimum interface

Before Durable Queue v2, a QueueAdapter boundary must exist with these operations:

- enqueue(command)
- claim(worker_instance_id)
- ack(command_id, run_id)
- fail(command_id, run_id, error_class, next_action)
- heartbeat(worker_instance_id, command_id)

The first adapter may wrap the legacy queue, but new supervisor code must use the adapter boundary instead of touching legacy queue internals directly.

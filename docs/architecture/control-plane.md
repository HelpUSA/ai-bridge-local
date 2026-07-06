---
type: architecture
status: current
tags:
 - architecture
 - control-plane
---

# Control plane architecture

AI Bridge Local is moving from command relay to durable local control plane.

## Target flow

```text
Chat / agent
 -> browser extension thin adapter
 -> local event ingest API
 -> AI Bridge Local control plane
 -> queue adapter and durable runs
 -> worker supervisor
 -> worker executor
 -> result summarizer
 -> browser action
 -> chat summary


## Core principles

1. The extension is a browser adapter, not a control plane.
2. AI Bridge Local is the only authority for workflow state and decisions.
3. Every command and browser action must be idempotent or deduped.
4. Intermediate events do not automatically generate chat replies.
5. Final events may generate replies only under explicit policy.
6. Full logs remain local; chats receive short summaries by default.
7. Security decisions are recorded before risky execution.

## Recommended local modules

- chat_state_manager.py: durable state per chat and task.
- browser_event_store.py: append-only browser events and snapshots.
- browser_action_manager.py: actions to be executed by the extension.
- queue_adapter.py: stable queue interface for current and future queues.
- worker_supervisor.py: heartbeat, stale PID recovery and restart policy.
- recipe_runner.py: approved local workflows.
- result_summarizer.py: concise summaries and local log references.
- security_gate.py: allowlists, risk levels and redaction.

## Migration rule

Legacy behavior remains available until the thin adapter flow has equivalent smoke coverage. New orchestration features must target AI Bridge Local, not the browser extension.

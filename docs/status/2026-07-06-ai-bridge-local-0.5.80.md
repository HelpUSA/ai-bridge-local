# AI Bridge Local 0.5.80 - BrowserAction persistence and QueueAdapter minimum

Date: 2026-07-06

## Summary

0.5.80 adds the first persisted BrowserEvent/BrowserAction v1 surface to the local gateway and introduces a minimal QueueAdapter compatibility layer over the existing `commands` table.

The change is intentionally additive and conservative:

- Existing `/bridge/commands`, `/bridge/next-action`, and `/bridge/acks` behavior remains unchanged.
- Browser events are persisted in `browser_events`.
- Browser actions are persisted in `browser_actions`.
- Browser actions have explicit result recording through `/browser/actions/result`.
- Control status now exposes browser event totals, browser action status counts, and recent browser rows.
- `queue_adapter.py` provides a small enqueue/claim/ack/fail/heartbeat API for later durable queue work.

## New gateway endpoints

- `POST /browser/events`
- `POST /browser/actions`
- `GET /browser/actions/next?chat_id=<chat_id>`
- `POST /browser/actions/result`

## Validation

Validated with:

```text
python -m py_compile gateway_local.py queue_adapter.py scripts/watcher/smoke_0580_browser_actions_queue_adapter.py
python scripts/watcher/smoke_0580_browser_actions_queue_adapter.py
git diff --check
```

## Notes

This release does not refactor the worker to consume QueueAdapter yet. That remains a later worker-supervisor/durable-queue task.

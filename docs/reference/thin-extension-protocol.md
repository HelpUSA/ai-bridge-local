---
type: reference
status: draft
tags:
 - extension
 - protocol
 - browser-events
---

# Thin extension protocol

The browser extension forwards browser facts to AI Bridge Local and executes simple browser actions requested by AI Bridge Local.

## BrowserEvent v1

Browser events are append-only and idempotent.

Required fields:

```json
{
 "schema_version": 1,
 "event_id": "uuid-or-stable-id",
 "event_type": "browser.message_observed",
 "trace_id": "trace-or-task-id",
 "chat_id": "chat-id",
 "platform": "chatgpt",
 "tab_id": "browser-tab-id",
 "url": "current-url",
 "observed_at": "iso-8601",
 "dedupe_key": "stable-dedupe-key",
 "payload_json": {}
}


Initial event types:

- browser.chat_snapshot
- browser.message_observed
- browser.generation_started
- browser.generation_finished
- browser.ui_error_detected
- browser.action_result
- browser.tab_available
- browser.tab_unavailable

## BrowserAction v1

Browser actions are requested by AI Bridge Local and executed by the extension.

Required fields:

```json
{
 "schema_version": 1,
 "action_id": "uuid-or-stable-id",
 "action_type": "browser.inject_message",
 "trace_id": "trace-or-task-id",
 "chat_id": "chat-id",
 "requested_at": "iso-8601",
 "deadline_at": "iso-8601",
 "status": "requested",
 "payload_json": {},
 "result_json": {}
}


Initial action types:

- browser.inject_message
- browser.focus_chat
- browser.open_chat
- browser.request_snapshot
- browser.noop

Action states:

```text
requested -> delivered_to_extension -> sent_to_chat
requested -> delivered_to_extension -> failed
requested -> unavailable
requested -> expired
requested -> deduped


Every BrowserAction must produce an action result. If the extension cannot confirm injection, it must report failed or unavailable instead of deciding a retry itself.

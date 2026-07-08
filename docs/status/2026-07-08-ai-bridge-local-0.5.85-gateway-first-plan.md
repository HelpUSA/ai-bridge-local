# AI Bridge Local 0.5.85 Gateway-first plan

Date: 2026-07-08

## Goal

Make the local gateway the primary control plane for AI Bridge Local. The browser extension should become thinner, and chats should stop carrying complex operational logic whenever the gateway can safely own it.

## Why

Recent failures came from chats manually building envelopes, handling JSON escaping, deciding retry strategy, and diagnosing delivery failures. Those responsibilities are better handled by local deterministic code.

## Target architecture

1. Gateway local as control plane
 - Own strict envelope validation.
 - Own command normalization.
 - Own routing decisions.
 - Own queue inspection.
 - Own duplicate detection and idempotency.
 - Own retry policy.
 - Own structured diagnostics.
 - Own post-run audit hooks.

2. Browser extension as thin transport
 - Register current chat id.
 - Capture/send browser messages.
 - Report delivery/capture failures.
 - Avoid owning business logic, retries, or envelope construction where possible.

3. Chats as intent senders
 - Prefer high-level intents instead of large hand-written envelopes.
 - Avoid raw multiline JSON.
 - Avoid manual escaping of Windows paths and code snippets.
 - Let gateway helper APIs produce final envelopes.

4. Control Center as operator UI
 - Show gateway health.
 - Show extension registration state.
 - Show runner status.
 - Show queue depth and stuck items.
 - Show recent commands and errors.
 - Provide retry, cancel, cleanup, and audit actions.

## Phase A: discovery and boundaries

Inventory existing gateway, runner, queue, extension, watcher scripts, and Control Center files. Produce a responsibility map: extension-owned, gateway-owned, runner-owned, script-owned, and chat-owned.

## Phase B: gateway APIs

Add or formalize endpoints for health, registered chats, queue status, command validation, command submission, retry, cancel, and diagnostics. Keep backward compatibility with current envelope format.

## Phase C: gateway envelope factory

Move JSON-safe envelope creation into gateway-accessible tooling or endpoint. Chats should be able to provide action intent and parameters; gateway returns or enqueues a validated envelope.

## Phase D: diagnostics

Return structured error categories: parse_error, source_chat_id_mismatch, target_not_registered, extension_capture_failed, runner_offline, command_failed, timeout, duplicate_command, unsafe_payload, and upstream_unsynced.

## Phase E: extension slimming

Remove or bypass extension logic that duplicates gateway responsibilities. Extension remains responsible for browser-specific actions only.

## Phase F: Control Center integration

Expose the new gateway APIs in Control Center. Add operator actions for retry, cleanup, queue inspection, registered chat inspection, and post-push audit.

## Safety constraints

- Do not break existing 0.5.83/0.5.84 envelope compatibility.
- Do not create a release until smoke tests and interchat tests pass.
- Do not change protocol semantics without a compatibility adapter.
- Keep local capability execution behind gateway validation.
- Keep audit logs structured and readable.

## First implementation candidate

Start with gateway-side introspection and validation endpoints because they reduce risk without changing browser delivery behavior. Then add gateway-owned envelope factory and queue diagnostics.

## Current local note

app_windows/controlcenter.bat may remain an unrelated local untracked helper unless intentionally added in a separate commit.

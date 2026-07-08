# AI Bridge Local 0.5.84 docs+tooling progress

Date: 2026-07-08

## Scope

0.5.84 is limited to docs and tooling. It does not change gateway runtime behavior, queue behavior, inter-chat protocol, or browser delivery behavior.

## Added

- `scripts/watcher/envelope_json_safe_helper.py`
  - Renders strict one-line JSON envelopes between bridge markers.
  - Supports `send-chat-message` and `run-command`.
  - Validates required schema, action, and delivery fields before output.

- `scripts/smoke/smoke_envelope_json_safety.py`
  - Confirms generated envelope JSON stays on one physical line.
  - Confirms multiline message content is encoded safely inside JSON.
  - Confirms raw Windows backslashes in hand-written JSON are rejected.
  - Confirms physically multiline JSON bodies are rejected.

- `scripts/watcher/post_push_auditor.py`
  - Generic post-push repository audit helper.
  - Checks expected files, git status, and upstream synchronization when available.

## Validation

The helper compiles and generated a valid marked run-command envelope.

The smoke passed:

```text
SMOKE_ENVELOPE_JSON_SAFETY_START
SMOKE_ENVELOPE_JSON_SAFETY_OK
```

The post-push auditor passed in dirty/skip-upstream mode while validating the expected 0.5.84 files.

## Commit note

`app_windows/controlcenter.bat` is an unrelated untracked local helper and must not be included in the 0.5.84 docs+tooling commit.

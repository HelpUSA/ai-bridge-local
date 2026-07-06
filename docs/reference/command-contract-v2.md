---
type: reference
status: draft
tags:
 - command-contract
 - recipes
 - payload-ref
---

# Command Contract v2

Command Contract v2 reduces long chat messages and moves verbose payloads to local durable references.

## Goal

Chats should express intent. AI Bridge Local expands intent into validation, scripts, execution, logs, summaries and delivery.

## Compact command shape

Required fields:

- schema: ai_bridge_local.command
- schema_version: 2
- command_id
- trace_id
- source
- target
- intent
- recipe
- payload_ref
- policy

Example shape:

schema = ai_bridge_local.command
schema_version = 2
command_id = stable id
trace_id = trace id
source = current_chat
target = gateway
intent = recipe.run
recipe = safe_patch_test_commit
payload_ref = local durable payload reference
policy.reply_on_final = true
policy.risk_level = write

## Rules

- source_chat_id may be inferred when the event originates from the extension.
- Targets may use aliases such as gateway, current_chat or saved chat aliases.
- Long payloads are stored locally and referenced by payload_ref.
- Inline payload size is limited.
- Schema validation errors are final corrigible errors.
- Commands must be deduped by command_id or payload hash.
- Legacy envelopes remain accepted during migration.

## Compatibility

New recipes should internally use this contract even before all chats emit v2 commands directly.

---
type: operational-status
status: current
date: 2026-07-01
component: ai-bridge-local
version: 0.5.70
head:
18aebef
origin_main:
18aebef
tags:
 - status
 - watcher
 - ai-bridge-local
 - continuation
---

# AI Bridge Local 0.5.70 operational status

## Current state

- Repository is synchronized: HEAD
18aebef
 and origin/main
18aebef
.
- VERSION is 0.5.70.
- Manifest is AI Bridge Local 0.5.70.
- Active content script constants are aligned to 0.5.70.
- Parse errors after reload now report versao=0.5.70.
- Final AI_LOCAL_RUN messages now use no_reply=0 when chat_can_continue=1.
- Queued gateway feedback remains no_reply=1.

## Confirmed live checks

- post_reload_live_smoke_0570_20260701_001 returned no_reply=0, result_is_final=1, success=1 and chat_can_continue=1.
- invalid_parse_version_probe_0570_20260701_001 returned AI_LOCAL_ERRO with versao=0.5.70.
- interchat_live_0570_after_reload_20260701_003 returned sent_direct with versao=0.5.70.

## Commits included

- a77c9e0 extension: treat duplicate commands idempotently.
- 4c7c184 extension: bump local bridge to 0.5.68.
- 359d36e worker: wake chat on final local run result.
- ccd0ca7 docs: document local bridge continuation fixes.
- 6cf033a gateway: wake chat on final fallback results.
- 682038c docs: document gateway final continuation fix.
- 18aebef extension: align content script internal versions.

## Validation history

- py_compile passed for gateway_local.py and brain_worker.py.
- node --check passed for extension/background.js, extension/content_script.js and extension/route_classifier.js.
- smoke_gateway_final_run_no_reply_0570 passed.
- smoke_final_run_continue_no_reply_0569 passed.
- smoke_post_command_duplicate_idempotent_0570 passed.
- smoke_content_script_internal_versions_0570 passed.
- smoke_direct_interchat_router_0542 passed.
- smoke_gateway_feedback_dedup passed.
- smoke_command_accepted_progress_notice passed.

## Remaining recommendations

- Keep extension reload as mandatory after version changes.
- Add a future watchdog for commands stuck in queued or delivering states.
- Continue improving Gemini watcher separately after the ChatGPT inter-chat path remains stable.

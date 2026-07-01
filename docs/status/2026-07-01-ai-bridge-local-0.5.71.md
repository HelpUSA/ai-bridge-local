---
type: operational-status
status: current
date: 2026-07-01
component: ai-bridge-local
version: 0.5.71
head: 49c3fb3
7ed6d5e
origin_main: 49c3fb3
7ed6d5e
tags:
 - status
 - watcher
 - ai-bridge-local
 - interchat
---

# AI Bridge Local 0.5.71 operational status

## Current state

- Repository is synchronized: HEAD 49c3fb3 and origin/main 49c3fb3.
7ed6d5e
 and origin/main
7ed6d5e
.
- VERSION is 0.5.71.
- Manifest is AI Bridge Local 0.5.71.
- Active extension constants are aligned to 0.5.71.
- Final AI_LOCAL_RUN still returns no_reply=0 when chat_can_continue=1.
- Inter-chat direct delivery using target_url returned sent_direct with versao=0.5.71.

## Confirmed live checks

- post_reload_live_smoke_0571_20260701_001 returned no_reply=0, result_is_final=1, success=1 and chat_can_continue=1.
- interchat_live_0571_target_url_20260701_003 returned sent_direct with versao=0.5.71.

## Fix delivered

- Direct delivery refreshes target tab discovery before sending.
- Target discovery prefers active matching tabs.
- This reduces the chance of result_to messages being delivered to an old or duplicate tab.

## Next recommendation

- 0.5.72 should harden parsing or diagnostics for raw control characters and line breaks inside JSON string fields.

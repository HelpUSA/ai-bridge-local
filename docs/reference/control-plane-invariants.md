---
type: reference
status: current
tags:
 - invariants
 - control-plane
---

# Control plane invariants

These invariants protect the AI Bridge Local architecture during migration.

1. The extension never decides workflow retry.
2. The extension service worker is never the source of truth.
3. AI Bridge Local is the authority for chat task, command, run and browser action state.
4. Ack happens only after a final result is persisted.
5. Every BrowserAction requires an action result.
6. Every command has a stable command_id and dedupe or idempotency strategy.
7. Full logs stay local by default.
8. Chat replies use summaries, not full stdout/stderr, unless explicitly requested.
9. no_reply=1 must not generate a chat reply without explicit override policy.
10. queued is intermediate.
11. AI_LOCAL_RUN is final.
12. Pre-gateway parse errors are final corrigible errors.
13. queued_timeout is a final post-gateway failure.
14. Worker kill requires strong validation; stale PID removal without kill may be automatic.
15. Auto-resume requires cooldown, dedupe_key and max_resumes_per_task.
16. Security risk level is recorded before write, destructive, network or secret-touching actions.

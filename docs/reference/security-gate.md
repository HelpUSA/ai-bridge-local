---
type: reference
status: draft
tags:
 - security
 - safety
 - redaction
---

# Security gate

The security gate is progressive. It starts as documented policy and becomes enforced by queue v2, command contract v2 and recipes.

## Risk levels

- read: inspect files, logs or status.
- write: modify allowlisted files.
- destructive: delete, reset, kill, clean or overwrite broad paths.
- network: deploy, download or call external services.
- secret: read or expose credentials, tokens or private data.

## Baseline policy

- No git add dot.
- Stage exact files only.
- Write actions require explicit cwd and file allowlist.
- Destructive actions require human confirmation.
- Logs are local by default.
- Summaries must pass redaction before chat delivery.
- Secrets are never intentionally pasted back into chats.

## Security decision record

Queue v2 should persist:

- risk_level
- security_decision
- allowed_by
- allowlist_match
- requires_human
- redaction_applied
- blocked_reason

## Migration

- 0.5.79 documents allowlists and forbidden patterns.
- 0.5.82 persists security_decision and risk_level.
- 0.5.83 validates cwd, action and payload size.
- 0.5.84 recipes are allowlisted.
- 0.5.85 applies redaction before chat summaries.

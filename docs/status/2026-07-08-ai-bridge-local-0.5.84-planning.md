# AI Bridge Local 0.5.84 Planning

Status: planning only. No release is being created now.

## Context
- 0.5.83 is operational and closed successfully.
- Gateway runtime confirmed at 0.5.83 on port 8766.
- Health endpoint returned 200.
- Repository was clean before this planning doc.
- smoke_version_alignment passed.
- Interchat sync was delivered and acknowledged.
- focused_target_interchat_audit_20260708_001 failed because of the audit script itself, not because of protocol or gateway failure.

## Decision
- Do not change the main protocol path without new evidence.
- Do not create a 0.5.84 release from this planning note.
- Limit 0.5.84 scope to docs and tooling.

## Planned scope
1. JSON-safe envelope helper.
2. Smoke test against raw Windows backslash inside JSON strings.
3. Smoke test against invalid multiline JSON strings.
4. Generic post-push auditor.
5. Documentation for safe helper usage.

## Acceptance criteria
- Helper produces strict JSON between bridge markers.
- Helper prevents raw backslash and control-character failures observed in 0.5.83 operations.
- Smokes fail on malformed envelopes before they reach live operations.
- Post-push auditor can be reused across projects.
- No protocol behavior changes are introduced.

## Notes from closeout
- Common operational errors: envelope_parse_error, composer_not_empty_before_inject, inject_timeout, content_script_reinject_failed.
- Operational delivery errors alone are not evidence for protocol changes.

End.

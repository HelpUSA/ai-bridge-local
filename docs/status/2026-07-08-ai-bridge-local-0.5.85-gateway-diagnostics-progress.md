# AI Bridge Local 0.5.85 gateway diagnostics progress

Date: 2026-07-08

## Scope

This is the first implementation step of the 0.5.85 Gateway-first plan.

The change keeps current envelope compatibility and does not alter queue execution, runner behavior, browser delivery, or extension routing.

## Added

- fetch_gateway_diagnostics() in gateway_local.py.
- GET /control/diagnostics endpoint.
- scripts/smoke/smoke_gateway_control_diagnostics.py.

## Gateway-first intent

The endpoint gives the local gateway a consolidated operator view so chats and the extension do not need to infer state from scattered commands or partial errors.

The response includes:

- gateway-first control-plane ownership markers;
- compatibility marker for 0.5.83-style envelopes;
- queue counts;
- active targets and sources;
- browser action status;
- recent browser actions;
- dead-letter count;
- recent command errors;
- recommended next diagnostic checks.

## Validation

Validated with:

text
python -m py_compile gateway_local.py scripts/smoke/smoke_gateway_control_diagnostics.py
python scripts/smoke/smoke_gateway_control_diagnostics.py
python scripts/watcher/post_push_auditor.py --allow-dirty --skip-upstream ...
git diff --check


Smoke result:

text
SMOKE_GATEWAY_CONTROL_DIAGNOSTICS_START
SMOKE_GATEWAY_CONTROL_DIAGNOSTICS_OK


## Safety notes

- No release was created.
- Existing gateway endpoints remain compatible.
- Existing envelope protocol remains unchanged.
- The browser extension remains unchanged in this step.
- app_windows/controlcenter.bat remains an unrelated local untracked helper and must stay outside this commit.

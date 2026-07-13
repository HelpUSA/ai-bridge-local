# AI Bridge Local 0.5.85 — extension gateway-only dispatch

Date: 2026-07-13

## Result

The active extension dispatch path no longer selects between `direct_interchat` and
`local_gateway`.

- `aiBridgeClassifyRouteSafe()` is now a compatibility shim that always returns
  `local_gateway`.
- `routeBridgeCommand()` always submits commands to `/bridge/commands`.
- Captured envelopes use the same gateway submission path.
- Route ownership remains in `gateway_local.py`.
- Browser injection helpers remain temporarily available only for actions claimed
  and delivered by the gateway.

## Guardrail

`scripts/smoke/smoke_extension_gateway_only_dispatch.py` prevents either active
dispatcher from regaining a direct-interchat branch.

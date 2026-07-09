# AI Bridge Local 0.5.85 Control Center diagnostics integration

Date: 2026-07-09

## Scope

This step wires the Windows Control Center to the new gateway-first diagnostics endpoint.

## Changed

- Added `DIAGNOSTICS_URL` pointing to `GET /control/diagnostics`.
- Updated `fetch_status()` to try diagnostics first.
- Kept fallback to the older `GET /control/status` endpoint.
- Updated the dashboard to render gateway-first markers, queue diagnostics, active targets, dead-letter count, recent error count, and recommended checks.
- Updated refresh summary to support both the legacy `command_status` shape and the new `queue` shape.
- Added `scripts/smoke/smoke_control_center_diagnostics_integration.py`.

## Safety notes

- Existing `/control/status` remains supported.
- The Control Center still works with older gateways through fallback.
- No browser extension behavior changed.
- No queue, runner, or envelope behavior changed.

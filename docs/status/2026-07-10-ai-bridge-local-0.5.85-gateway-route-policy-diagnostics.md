# AI Bridge Local 0.5.85 gateway route policy diagnostics

Date: 2026-07-10

## Scope

This step makes the gateway-first route policy explicit in gateway diagnostics and visible in the Control Center.

## Changed

- Added `route_policy` to `fetch_gateway_diagnostics()`.
- Declared `gateway_first` as the active route mode.
- Declared direct interchat as blocked by default.
- Declared `local_gateway` as the replacement route for direct interchat.
- Declared `local_gateway` as the route for inter-agent messages and local capability commands.
- Updated Control Center rendering to show route policy, direct interchat status, block reason, and route lock.
- Added `scripts/smoke/smoke_gateway_route_policy_diagnostics.py`.

## Remaining work

The next step is to convert this diagnostic declaration into an executable gateway-owned route-decision helper/API.

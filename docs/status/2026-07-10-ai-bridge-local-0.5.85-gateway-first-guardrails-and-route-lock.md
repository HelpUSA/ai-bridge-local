# AI Bridge Local 0.5.85 gateway-first guardrails and route lock

Date: 2026-07-10

## What changed

This checkpoint continues the gateway-first migration after the default direct interchat cutoff.

Implemented:

- Added a static route lock around `globalThis.aiBridgeClassifyRouteSafe`.
- When `DIRECT_INTERCHAT_ENABLED=false`, any route classified as `direct_interchat` is converted to `local_gateway`.
- Added local telemetry on the blocked route with:
  - `reason`
  - `route=local_gateway`
  - `blocked_route=direct_interchat`
  - `action`
  - `delivery_kind`
  - timestamp
- Added guardrail smoke tests:
  - `scripts/smoke/smoke_gateway_first_direct_interchat_disabled.py`
  - `scripts/smoke/smoke_gateway_first_route_guardrails.py`

## Current practical state

The gateway now has stronger control in three layers:

1. Gateway diagnostics and queue visibility exist through `/control/diagnostics`.
2. Control Center already prefers gateway diagnostics over the older status endpoint.
3. The Chrome extension no longer defaults to direct interchat delivery and now also blocks route-classifier side exits to `direct_interchat` while gateway-first mode is active.

## Remaining work

The extension still contains legacy direct interchat implementation paths as opt-in code. This is acceptable for the current checkpoint, but the long-term goal remains to move route decision and delivery policy out of the extension and into the gateway.

Next recommended improvements:

1. Persist blocked-route telemetry in gateway diagnostics instead of console/global state only.
2. Add a gateway route-decision endpoint or internal route-decision service.
3. Make the extension request or follow gateway decisions instead of owning route policy.
4. Expand Control Center to show:
   - `direct_interchat_enabled`
   - `direct_interchat_disabled_reason`
   - last blocked route
   - recent route decisions
5. Run live end-to-end checks for:
   - `run-command/local_capability`
   - `send-chat-message/inter_agent_message`
   - missing target
   - reload/reconnect
   - queue persistence
   - dead letter path

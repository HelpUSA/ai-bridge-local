# AI Bridge Local 0.5.85 executable gateway route decisions

Date: 2026-07-13

## Scope

This step converts the declared gateway-first route policy into executable gateway behavior.

## Implemented

- Added `get_gateway_route_policy()` as the shared policy source for diagnostics and routing.
- Added `decide_gateway_route(body, payload=None)`.
- Added `GET /control/route-policy`.
- Added `POST /control/route-decision`.
- Applied the route decision before every `/bridge/commands` enqueue.
- Included the resolved `route_decision` in successful enqueue responses.
- Preserved inter-agent destination chat IDs while routing through `local_gateway`.
- Forced local-capability commands to `gateway-brain-supervisor`.
- Blocked a requested `direct_interchat` route and replaced it with `local_gateway`.
- Added `scripts/smoke/smoke_gateway_route_decision.py`.

## Route outcomes

| Delivery kind | Executable route | Target behavior | Executor role |
| --- | --- | --- | --- |
| `inter_agent_message` | `local_gateway` | Preserve destination chat | `thin_transport_executor` |
| `local_capability` | `local_gateway` | Force `gateway-brain-supervisor` | `local_capability_executor` |

The gateway remains the decision owner. The extension executes transport work but no longer owns route selection.

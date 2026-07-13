# Gateway-first control plane operations

Date: 2026-07-10

## Operating model

- Chat tabs send intent.
- Gateway validates, queues, routes and diagnoses.
- Extension transports messages and executes browser actions.
- Control Center reads gateway diagnostics as source of truth.

## First checks

1. Open Control Center.
2. Confirm diagnostics endpoint is `/control/diagnostics`.
3. Confirm gateway-first mode is visible.
4. Check queue counts, active targets/sources, recent errors and dead letters.

## Direct interchat policy

Direct interchat is not the default path.

Expected markers in `extension/background.js`:

- `const DIRECT_INTERCHAT_ENABLED = false;`
- `const DIRECT_INTERCHAT_DISABLED_REASON = "gateway_first_control_plane_owns_delivery";`
- `return !DIRECT_INTERCHAT_ENABLED;` for `send-chat-message` / `inter_agent_message`.

## When a message does not arrive

Check gateway diagnostics, queue counts, active targets, recent errors, dead letters, extension registration, target tab registration and whether gateway-first policy intentionally blocks direct interchat.

## Safe patch pattern

Make the smallest behavior change, add smoke coverage, run syntax checks, run `git diff --check`, stage only expected files, commit, push, then run `scripts/watcher/post_push_auditor.py --allow-dirty`.

## Known local-only file

`app_windows/controlcenter.bat` should stay untracked by default.

<!-- 2026-07-10-route-lock-ops -->

## Route-lock operational checks

For gateway-first operations, keep these checks green before shipping route-related changes:

```bash
python scripts/smoke/smoke_gateway_first_direct_interchat_disabled.py
python scripts/smoke/smoke_gateway_first_route_guardrails.py
node --check extension/background.js
```

Expected extension markers:

- `DIRECT_INTERCHAT_ENABLED=false`
- `DIRECT_INTERCHAT_DISABLED_REASON=gateway_first_control_plane_owns_delivery`
- `mustUseGateway()` returns `!DIRECT_INTERCHAT_ENABLED` for `send-chat-message/inter_agent_message`
- `aiBridgeClassifyRouteSafe` is wrapped by the gateway-first route lock
- blocked `direct_interchat` classifications are converted to `local_gateway`

Operational interpretation:

- `local_capability` continues to be gateway-only.
- `send-chat-message/inter_agent_message` should not use direct interchat by default.
- Any direct-interchat attempt while disabled should be treated as a route-policy event, not a delivery path.

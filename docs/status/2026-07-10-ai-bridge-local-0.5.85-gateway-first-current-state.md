# AI Bridge Local 0.5.85 gateway-first current state

Date: 2026-07-10

## What is already done

- Gateway diagnostics endpoint `/control/diagnostics` exists and exposes gateway-first posture, queue state, active targets/sources, recent commands, recent errors, dead letters and recommended checks.
- Control Center now tries `/control/diagnostics` first and falls back to `/control/status`.
- Thin-extension audit is documented and shows the remaining extension-side ownership areas.
- The first functional gateway-first extension cut is pushed: `DIRECT_INTERCHAT_ENABLED = false`, `DIRECT_INTERCHAT_DISABLED_REASON` exists, and `mustUseGateway()` sends `send-chat-message` / `inter_agent_message` through the gateway while direct interchat is disabled.

## Practical status

The application is no longer only in planning. It has a real gateway-first behavior change. Inter-agent messages now prefer the gateway by default, but the migration is not complete.

## Remaining risks

- Direct interchat implementation still exists as legacy/opt-in code.
- The route-classifier wrapper still needs a hard guard so any `direct_interchat` decision becomes `local_gateway` while direct interchat is disabled.
- Control Center still needs to show direct-interchat effective mode and disabled reason.
- End-to-end flows still need a dedicated gateway-first validation pass.

## Related commits

- `ccaa1f7 feat: add gateway diagnostics endpoint`
- `e3a37cf feat: wire control center diagnostics`
- `bd58d70 docs: add thin extension gateway audit`
- `8e7c3d8 feat: default direct interchat to gateway`

## Known local-only file

`app_windows/controlcenter.bat` is expected to remain untracked unless explicitly requested.

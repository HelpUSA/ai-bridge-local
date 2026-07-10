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

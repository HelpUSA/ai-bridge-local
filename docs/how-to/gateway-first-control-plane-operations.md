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

## Official Control Center launcher artifacts

`app_windows/controlcenter.bat` and
`app_windows/controlcenter_launcher.ps1` are official project artifacts and
must be tracked together.

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

## Reading route policy in Control Center

The Control Center reads `/control/diagnostics` first. When available, it displays:

- `Politica de rota`
- direct interchat status
- direct interchat disabled reason
- inter-agent route
- local capability route
- route lock mapping from `direct_interchat` to `local_gateway`

If these fields are missing, verify that the gateway is running the version containing `route_policy` in `fetch_gateway_diagnostics()`.

## Executable route-decision endpoints

Use `GET /control/route-policy` to inspect the active gateway-owned policy.

Use `POST /control/route-decision` with a JSON body containing at least `delivery_kind` and `target_chat_id` to preview the route without enqueueing a command.

Normal command submission through `POST /bridge/commands` now applies the same helper before persistence and returns a `route_decision` object. For `local_capability`, the persisted target is always `gateway-brain-supervisor`. For `inter_agent_message`, the destination chat is preserved while the route remains `local_gateway`.

A payload or body requesting `direct_interchat` is reported as blocked and replaced by `local_gateway`.

## Extension gateway-only dispatch

The extension is a thin transport/executor. New commands and captured envelopes are
submitted to the local gateway through `POST /bridge/commands`.

The extension must not choose `direct_interchat`. Route policy and normalization are
owned by:

- `GET /control/route-policy`
- `POST /control/route-decision`
- `POST /bridge/commands`

Browser-side injection helpers execute actions claimed from the gateway; they are not
an alternative control plane.

## 2026-07-13 ? extens?o sem decis?o local de rota

A extens?o agora possui apenas um caminho de despacho: todo envelope ?
enviado para `/bridge/commands` por `routeBridgeCommand`. Os antigos
helpers de classifica??o direta, descoberta de aba, entrega interchat e
fallback direto foram removidos.

`injectText` e sua l?gica de reinje??o continuam presentes porque fazem
parte do executor de a??es entregues pelo gateway. Eles n?o escolhem a
rota e n?o permitem que a extens?o contorne o plano de controle.

Refer?ncias anteriores a `DIRECT_INTERCHAT_ENABLED` ou `mustUseGateway`
neste hist?rico descrevem a fase intermedi?ria da migra??o e n?o o
estado atual.

<!-- AI_BRIDGE_MANAGED:CONTROL_CENTER_OPERATIONS_0585:START -->

## Control Center recovery and diagnostics

The official paired launcher artifacts are:

- `app_windows/controlcenter.bat`;
- `app_windows/controlcenter_launcher.ps1`.

Running the BAT closes only an existing visible, hidden or stale Control Center
process. Gateway and worker are preserved. The launcher waits for the UI mutex
and starts exactly one new Control Center instance.

The Control Center starts gateway and worker when they are absent.

Health interpretation:

- `queued` and `delivering` represent current active work;
- `fila_ativa` is their sum;
- `acked`, `failed` and `dead_letters` are historical totals;
- historical totals do not mean the current queue is unhealthy;
- historical `acked` can use a read-only query against `queue_local.db`.

HTTP requests, process scans, database reads and log reads run outside the Tk
thread. Widget updates remain on the main Tk thread.

Ports:

- `8766`: legacy transport, acknowledgements and diagnostics;
- `8767`: compact command plane.

`local.run` remains disabled unless explicitly enabled and confirmed.

<!-- AI_BRIDGE_MANAGED:CONTROL_CENTER_OPERATIONS_0585:END -->

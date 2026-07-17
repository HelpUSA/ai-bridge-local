# AI Bridge Local gateway-first roadmap

Date: 2026-07-10

## Goal

Make the gateway the control plane. Chats send intent. Gateway validates, queues, routes, retries and diagnoses. The extension becomes thin transport plus browser-action executor. Control Center reads gateway truth.

## Completed

1. Gateway diagnostics endpoint.
2. Control Center diagnostics-first integration.
3. Thin-extension audit.
4. Direct interchat disabled by default for normal inter-agent delivery.

## Next activities

### M5: Guardrails for the current extension cut

- Add smoke for `DIRECT_INTERCHAT_ENABLED = false`.
- Add smoke for `DIRECT_INTERCHAT_DISABLED_REASON`.
- Add smoke for `return !DIRECT_INTERCHAT_ENABLED` in `mustUseGateway()`.
- Acceptance: re-enabling direct interchat by default fails tests.

### M6: Route-classifier gateway-first enforcement

- Add effective-route wrapper.
- Convert `direct_interchat` to `local_gateway` while direct interchat is disabled.
- Cover explicit `transport: direct`, `direct_interchat`, and default inter-agent messages.

### M7: Gateway route-decision service

- Add gateway-side route decision function or endpoint.
- Store route decision and reason in command metadata.
- Expose recent route decisions in `/control/diagnostics`.

### M8: Control Center visibility

- Show gateway-first mode.
- Show direct-interchat enabled/disabled.
- Show disabled reason.
- Show recent route decisions, dead letters and retry recommendations.

### M9: Extension responsibility reduction

- Keep tab discovery only for browser actions.
- Remove or isolate legacy direct-interchat helpers after opt-in period.
- Prevent new queue ownership logic in the extension.

### M10: End-to-end validation

Validate local capability, inter-agent message, missing target, reload, gateway restart, duplicate command id, dead letter and Control Center diagnostics.

## Release checklist

- [ ] Guardrail smoke committed.
- [ ] Route-classifier enforcement committed.
- [ ] Gateway route-decision diagnostics committed.
- [ ] Control Center displays effective direct-interchat mode.
- [ ] End-to-end smoke suite passes.
- [ ] Post-push auditor passes.

<!-- 2026-07-10-route-lock-update -->

## 2026-07-10 update: route lock checkpoint

Completed after the current-state documentation:

- Guardrail tests now protect the direct-interchat cutoff.
- A route lock converts `direct_interchat` classifications to `local_gateway` while `DIRECT_INTERCHAT_ENABLED=false`.
- The extension records a local blocked-route event for diagnostics follow-up.

### Updated implementation order

1. Keep the route lock and direct-interchat-disabled guardrails green on every gateway-first change.
2. Move blocked-route telemetry from extension-local state into gateway diagnostics.
3. Introduce gateway-owned route decision records.
4. Let Control Center render recent route decisions and blocked direct-interchat attempts.
5. Gradually reduce `extension/background.js` to capture, browser-action execution, and result reporting.

## 2026-07-10 update: route policy diagnostics

Completed after the route lock:

- Gateway diagnostics now include an explicit `route_policy` block.
- Control Center renders route policy and direct interchat block reason.
- The active policy declares `local_gateway` as the route for inter-agent messages and local capability commands.
- Remaining roadmap item: convert diagnostic route policy into an executable gateway-owned route-decision helper/API.

## 2026-07-13 update: executable route decisions

Completed:

- shared gateway route-policy helper;
- executable route-decision helper;
- route-policy and route-decision control endpoints;
- route decision applied before command enqueue;
- local capability target enforcement;
- direct interchat request replacement with `local_gateway`.

Next: add an end-to-end HTTP harness that starts an isolated gateway, submits route-decision and command requests, and verifies persisted queue targets.

## 2026-07-13 — extension gateway-only dispatch

Completed:

- removed the active direct-interchat branch from `routeBridgeCommand()`;
- routed captured envelopes through the same gateway command endpoint;
- reduced the extension classifier to a compatibility shim returning `local_gateway`;
- added a smoke guardrail against extension-owned route selection.

Next cleanup: remove unreachable legacy direct-dispatch helpers after gateway E2E
browser-action coverage proves they are no longer required.

## Conclu?do em 2026-07-13 ? remo??o do caminho direto ?rf?o

- removido o classificador local `route_classifier.js`;
- removidos os entry points de entrega interchat direta;
- removida a descoberta local de aba para roteamento;
- removidos os fallbacks locais direto ? gateway;
- preservado o executor de browser actions, incluindo `injectText`;
- adicionados guardrails que falham caso a extens?o volte a assumir
  decis?o de rota.

A pr?xima etapa ? ampliar a cobertura ponta a ponta do ciclo
gateway ? fila ? executor da extens?o ? ACK.

<!-- AI_BRIDGE_MANAGED:ROADMAP_RECONCILIATION_0585:START -->

## 2026-07-16 checkpoint: command plane and Control Center

Implementation work previously listed as M5 through M9 is complete:

- gateway-first route guardrails and executable route decisions;
- extension gateway-only dispatch during normal operation;
- obsolete extension-owned direct dispatch removed;
- legacy transport and diagnostics on port `8766`;
- compact command plane on port `8767`;
- additive `bridge2_*` durable storage;
- leases, retries, dead letters and persistent idempotency;
- Control Center autostart, single-instance mutex and recovery launcher;
- asynchronous UI refresh outside the Tk thread;
- active queue separated from historical counters;
- nine stale legacy queued commands archived without replay or deletion.

### Current roadmap position

The active roadmap item is M10: integrated end-to-end validation.

Next sequence:

1. add Control Center and launcher regression tests;
2. add an isolated HTTP harness for ports `8766` and `8767`;
3. validate persistence, targets, idempotency, leases, retries and dead letters;
4. run browser interchat and read-only local-capability checks;
5. prepare a commit only after explicit operator authorization.

<!-- AI_BRIDGE_MANAGED:ROADMAP_RECONCILIATION_0585:END -->

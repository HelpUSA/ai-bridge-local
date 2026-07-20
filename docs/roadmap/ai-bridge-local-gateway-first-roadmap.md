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

<!-- AI_BRIDGE_MANAGED:M10_VALIDATION_CHECKPOINT_0585:START -->

## M10 final validation checkpoint - 0.5.85

M10 is complete.

Validated areas:

- gateway-first route policy;
- isolated legacy gateway HTTP lifecycle;
- isolated command-plane HTTP endpoints;
- Control Center mutex, autostart and asynchronous refresh;
- smart launcher behavior;
- live browser interchat delivery;
- live read-only local-capability delivery;
- deterministic probe cleanup;
- empty active queues after cleanup;
- consolidated automated regression suite.

The remaining activity is repository finalization: inspect the complete diff,
authorize the commit and push the validated changes.

<!-- AI_BRIDGE_MANAGED:M10_VALIDATION_CHECKPOINT_0585:END -->

<!-- AI_BRIDGE_MANAGED:M11_WATCHER_DELIVERY_0585:START -->

## M11 watcher delivery reliability

Status: baseline audit and contracts complete.

Next implementation package:

1. composer preflight;
2. safe injection;
3. observable submission confirmation;
4. bounded idempotent retries;
5. precise error classification;
6. duplicate prevention;
7. live interchat probe and exact cleanup.

<!-- AI_BRIDGE_MANAGED:M11_WATCHER_DELIVERY_0585:END -->

<!-- AI_BRIDGE_MANAGED:M11_ACTIVE_DELIVERY_RELIABILITY_0585:START -->

## M11 active watcher delivery reliability

Implemented:

- strict composer ownership;
- preservation of unrelated user drafts;
- visible-message idempotency;
- bounded transient retries;
- stable command identity;
- retry telemetry;
- ACK retry metadata;
- Node and Python regression tests.

Remaining acceptance activity:

- reload the unpacked extension;
- execute the live interchat probe;
- verify ACK and delivery token;
- remove only the probe records.

<!-- AI_BRIDGE_MANAGED:M11_ACTIVE_DELIVERY_RELIABILITY_0585:END -->

<!-- AI_BRIDGE_MANAGED:M11_TARGET_REGISTRATION_REPAIR_0586:START -->

## M11 completion ? exact target isolation

M11 is complete in release `0.5.86`.

Release: `0.5.86`

Live acceptance time: `2026-07-18T23:10:20.069551+00:00`

Confirmed target: `6a563525-4740-83e9-a8a1-212c8e5baf1e`

Live command: `m11_fixed_target_primary_20260718_225107_0bb256ee`

Observed acceptance:

- gateway-first selected `local_gateway`;
- original, routed and persisted target IDs matched;
- delivery used `button_click_confirmed`;
- delivery completed in one wrapper attempt;
- automatic target discovery was disabled;
- historical command and dead-letter fallback were disabled;
- one visible delivery was executed;
- probe database records were removed;
- the live acceptance suite passed 32 tests;
- release validation adds one explicit version test, bringing the suite to 33 tests.

The next roadmap activity is M12: safe transport for large command payloads.

<!-- AI_BRIDGE_MANAGED:M11_TARGET_REGISTRATION_REPAIR_0586:END -->

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

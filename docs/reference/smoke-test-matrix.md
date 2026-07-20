---
type: reference
status: draft
tags:
  - reference
  - smoke
  - tests
---

# Smoke test matrix

## Core/router

- parse envelope
- classify route
- direct_interchat sem gateway
- local_gateway para run-command
- force_gateway respeitado

## Adapters

Cada adapter deve validar:

- detectPage
- getChatId
- findComposer
- injectText
- clickSend
- captureOutboundEnvelope

<!-- AI_BRIDGE_MANAGED:COMMAND_PLANE_CONTROL_CENTER_SMOKES_0585:START -->

## Command plane and Control Center 0.5.85

| Area | Validation | State |
| --- | --- | --- |
| Command plane unit contract | `python -m pytest tests/test_gateway_command_plane_0585.py` | Implemented |
| Command plane smoke | `python scripts/smoke/smoke_gateway_command_plane_0585.py` | Implemented |
| Queue administration | `python scripts/maintenance/queue_admin_0585.py summary` | Implemented |
| Gateway diagnostics | `python scripts/smoke/smoke_gateway_control_diagnostics.py` | Implemented |
| Control Center compile | `python -m py_compile app_windows/control_center_app.py` | Implemented |
| Smart launcher validation | `app_windows/controlcenter.bat --validate` | Implemented |
| Control Center regression tests | autostart, mutex, async refresh and counters | Implemented |
| Isolated HTTP E2E | ports `8766`, `8767`, persistence and targets | Implemented |
| Live browser interchat | real gateway-first delivery with terminal ACK | Implemented |
| Live read-only capability | harmless Python token through `run-command` | Implemented |
| Probe cleanup | exact test IDs removed after validation | Implemented |

<!-- AI_BRIDGE_MANAGED:COMMAND_PLANE_CONTROL_CENTER_SMOKES_0585:END -->

<!-- AI_BRIDGE_MANAGED:M11_WATCHER_DELIVERY_0585:START -->

## M11 watcher delivery reliability

| Area | Validation | State |
| --- | --- | --- |
| Source audit | composer, command identity, send and retry inventory | Implemented |
| Static watcher contracts | `pytest tests/test_watcher_delivery_contract_0585.py` | Implemented |
| Guarded delivery state machine | active browser reliability patch | Next |
| Residual composer safety | unrelated text is preserved | Next |
| Duplicate retry prevention | one visible delivery per command | Next |
| Live interchat regression | delivery, ACK and exact cleanup | Next |

<!-- AI_BRIDGE_MANAGED:M11_WATCHER_DELIVERY_0585:END -->

<!-- AI_BRIDGE_MANAGED:M11_ACTIVE_DELIVERY_RELIABILITY_0585:START -->

## M11 active watcher delivery reliability

| Area | Validation | State |
| --- | --- | --- |
| User composer preservation | unrelated text is not cleared | Implemented |
| Visible-message idempotency | visible delivery returns success | Implemented |
| Bounded retries | maximum of three attempts | Implemented |
| Stable command identity | retries retain the command ID | Implemented |
| Retry telemetry | scheduled retries produce events | Implemented |
| Node behavioral smoke | delivery policy VM test | Implemented |
| Live browser probe | reload, delivery, ACK and cleanup | Pending reload |

<!-- AI_BRIDGE_MANAGED:M11_ACTIVE_DELIVERY_RELIABILITY_0585:END -->

<!-- AI_BRIDGE_MANAGED:M11_TARGET_REGISTRATION_REPAIR_0586:START -->

## M11 target isolation acceptance ? 0.5.86

| Validation | Result |
| --- | --- |
| UUID extracted from browser URL | Passed |
| Browser heartbeat registration | Passed |
| URL, chat ID and tab ID identity | Passed |
| Exact open-tab resolution | Passed |
| Missing target blocked | Passed |
| Duplicate matching tabs blocked | Passed |
| Historical fallback prohibited | Passed |
| Fixed-target live delivery | Passed |
| Wrapper delivery attempts | 1 |
| Probe database cleanup | Passed |
| Release version assertion | Added |
| Combined release suite | 33 tests |

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

<!-- AI_BRIDGE_MANAGED:M11_TARGET_REGISTRATION_REPAIR_0586:END -->

<!-- AI_BRIDGE_MANAGED:M12_LARGE_PAYLOAD_TRANSPORT_0587:START -->
## M12 safe large payload transport - 0.5.87

| Validation | Result |
| --- | --- |
| Small command remains inline | Implemented |
| Large command uploads JSON payload | Implemented |
| Compact command receives SHA-256 payload reference | Implemented |
| Existing payload reference passes through | Implemented |
| Command-plane durable payload round trip | Implemented |
| Legacy gateway boundary preserved | Implemented |
| Legacy QueueAdapter boundary preserved | Implemented |
| Brain Worker boundary preserved | Implemented |
| Node behavioral smoke | Added |
| Python contract tests | Added |
| Runtime reload verification | Pending publication |
<!-- AI_BRIDGE_MANAGED:M12_LARGE_PAYLOAD_TRANSPORT_0587:END -->

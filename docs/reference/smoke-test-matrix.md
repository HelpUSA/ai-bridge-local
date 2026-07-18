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

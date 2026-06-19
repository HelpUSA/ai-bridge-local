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

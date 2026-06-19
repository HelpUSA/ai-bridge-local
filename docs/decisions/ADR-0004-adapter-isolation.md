---
type: adr
status: proposed
tags:
  - adr
  - adapters
  - isolation
---

# ADR-0004: Isolate AI platform adapters

## Status

Proposed

## Context

Correcoes em ChatGPT podem quebrar Gemini, DeepSeek ou HelpUSAI quando o codigo fica acoplado.

## Decision

Cada IA deve ter adapter proprio e smokes proprios.

## Consequences

- Mudancas ficam contidas.
- Novas IAs entram sem reescrever adapters antigos.
- Mudancas no core exigem matriz completa de regressao.

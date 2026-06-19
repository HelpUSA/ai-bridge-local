---
type: adr
status: proposed
tags:
  - adr
  - router
  - extension
---

# ADR-0002: Keep extension in ai-bridge-local and isolate internal apps

## Status

Proposed

## Context

A extensao atual precisa conversar entre chats e tambem encaminhar comandos ao gateway local.

## Decision

Manter a extensao na pasta atual por enquanto, mas separar internamente:

- apps/talk-inter-chat
- apps/local-gateway-client
- adapters
- core/router

## Consequences

- Evita migracao prematura.
- Reduz risco de quebrar gateway ao mexer em interchat.
- Prepara extracao futura se necessario.

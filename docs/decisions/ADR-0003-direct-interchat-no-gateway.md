---
type: adr
status: proposed
tags:
  - adr
  - interchat
  - gateway
---

# ADR-0003: Direct interchat must not depend on local gateway

## Status

Proposed

## Context

Conversas entre chats precisam funcionar sem gateway local, sem fila e sem banco.

## Decision

send-chat-message entre chats deve usar rota direta por aba registrada, salvo force_gateway=true.

## Consequences

- Menor latencia.
- Menos acoplamento.
- Gateway local fica reservado para comandos e tarefas locais.

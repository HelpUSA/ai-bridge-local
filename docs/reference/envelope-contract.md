---
type: reference
status: draft
tags:
  - reference
  - envelope
  - contract
---

# Envelope contract

## Campos principais

- schema
- schema_version
- command_id
- transport
- action
- source_chat_id
- target_chat_id
- delivery_kind
- message
- payload
- force_gateway

## Transportes

- direct_interchat
- local_gateway

## Compatibilidade

Enquanto envelopes antigos existirem, o router pode inferir rota por action.

---
type: explanation
status: draft
tags:
  - architecture
  - extension
  - router
---

# Architecture overview

## Objetivo

Separar responsabilidades dentro da extensao atual do AI Bridge Local sem mover a extensao de pasta agora.

## Componentes

- Core/router
- App talk-inter-chat
- App local-gateway-client
- Adapters por IA
- Gateway local

## Decisao atual

A extensao continua dentro de ai-bridge-local, mas o codigo deve ser separado por dominio.

## Fronteiras

- Conversa entre chats nao deve depender do gateway local.
- Execucao de comandos locais deve passar pelo gateway local.
- Cada IA deve ter adapter isolado.

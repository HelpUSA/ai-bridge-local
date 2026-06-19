---
type: reference
status: draft
tags:
  - reference
  - transport
---

# Transport modes

## direct_interchat

Usado para conversa direta entre chats abertos no navegador.

## local_gateway

Usado para comandos locais, patches, smokes e inspecoes locais.

## Regra de prioridade

send-chat-message sem force_gateway deve ir para direct_interchat. run-command deve ir para local_gateway.

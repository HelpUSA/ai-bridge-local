---
type: explanation
status: draft
tags:
  - architecture
  - router
---

# Extension router

## Responsabilidade

O router interno decide se um envelope deve ir para conversa direta entre chats ou para o gateway local.

## Principios

- O router decide rota.
- Apps executam a rota.
- Adapters conhecem cada IA.
- Gateway local executa comandos locais.

## Rotas principais

- direct_interchat: conversa entre abas.
- local_gateway: execucao via gateway local.

---
type: reference
status: draft
tags:
  - reference
  - router
  - contract
---

# Router contract

## Responsabilidade

Decidir o caminho correto a partir do envelope.

## Rotas

| Condicao | Rota |
|---|---|
| transport=direct_interchat | apps/talk-inter-chat |
| transport=local_gateway | apps/local-gateway-client |
| action=send-chat-message sem force_gateway | apps/talk-inter-chat |
| action=run-command | apps/local-gateway-client |
| force_gateway=true | apps/local-gateway-client |

## Restricoes

- O router nao deve conhecer detalhes de ChatGPT, Gemini, DeepSeek ou HelpUSAI.
- O router nao deve executar comandos.
- O router nao deve manipular DOM diretamente.

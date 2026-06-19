# AI Bridge Local 0.5.46 - Disable legacy scanner and inline heartbeat guard

Data: 2026-06-19T13:17:10.251547+00:00

## Problema

Após o 0.5.45, a aba do ChatGPT ainda mostrou:

- `aiBridgeSafeCallSendChatHeartbeat is not defined`
- `sendTextToChat is not defined`

A causa provável era dupla:

1. O guard do heartbeat ainda podia ser chamado fora do escopo onde foi definido.
2. O scanner legado global ainda varria `document.body.innerText`, reprocessava envelopes antigos e chamava `send()`, que dependia de `sendTextToChat` fora do escopo.

## Correção

- Substitui chamadas de heartbeat por guard inline sem depender de funcao externa.
- Desativa o scanner legado global `extract(t).forEach(send)`.
- Mantém o scanner standalone com parser próprio e feedback visível.
- Preserva o gateway obrigatório para `run-command/local_capability`.

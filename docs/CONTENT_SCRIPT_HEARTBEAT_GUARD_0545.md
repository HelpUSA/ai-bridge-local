# AI Bridge Local 0.5.45 - Content script heartbeat guard

Data: 2026-06-19T13:14:00.088016+00:00

## Problema

Após o 0.5.44, a aba do ChatGPT mostrou:

`Uncaught ReferenceError: sendChatHeartbeat is not defined`

Esse erro pode interromper o restante do content script e impedir a instalação do scanner standalone.

## Correção

- Adiciona `aiBridgeSafeCallSendChatHeartbeat`.
- Substitui chamadas diretas `sendChatHeartbeat();` por chamada segura.
- Substitui `setInterval(sendChatHeartbeat, ...)` por wrapper seguro.
- Preserva o scanner standalone com feedback visível.
- Mantém run-command/local_capability via gateway/DB/worker.

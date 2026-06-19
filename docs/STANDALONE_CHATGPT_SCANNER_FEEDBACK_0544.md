# AI Bridge Local 0.5.44 - Standalone ChatGPT scanner with visible feedback

Data: 2026-06-19T13:09:29.585751+00:00

## Objetivo

Corrigir captura de envelopes do ChatGPT sem depender de funcoes internas do IIFE principal do content script.

## Mudancas

- Scanner standalone com parser proprio.
- Envia comandos usando `chrome.runtime.sendMessage` com `AI_BRIDGE_BRIDGE_COMMAND`.
- Injeta `[AI_LOCAL]` visivel no chat origem quando a rota direta entrega com sucesso.
- Injeta `[AI_LOCAL_ERRO]` visivel no chat origem quando a captura/rota direta falha.
- Marca candidatos existentes no bootstrap para evitar reenviar envelopes antigos.
- Mantem `run-command/local_capability` pelo gateway/DB/worker.

## Observacao

A rota direta continua controlada pelo background 0.5.42+.

# AI Bridge Local 0.5.41 - ChatGPT outbound envelope capture

Data: 2026-06-19T01:43:13.807596+00:00

## Objetivo

Adicionar captura outbound de envelopes locais emitidos em respostas do ChatGPT.

## Problema corrigido

O envio REST pelo gateway funcionava, mas envelopes escritos no chat ChatGPT atual não eram capturados, não saíam para o gateway e não geravam aviso.

## Mudança

- Observa páginas `chatgpt.com`.
- Aceita blocos:
  - `@@AI_BRIDGE_LOCAL_START@@ ... @@AI_BRIDGE_LOCAL_END@@`
  - `@@AI_BRIDGE_LOCAL_BEGIN ... @@AI_BRIDGE_LOCAL_END@@`
- Captura comandos JSON com `schema=ai_bridge_local.envelope`.
- Valida `source_chat_id` contra o chat atual.
- Envia comandos capturados via `AI_BRIDGE_BRIDGE_COMMAND`.
- Em caso de erro, tenta postar `[AI_LOCAL_ERRO]` no próprio chat.

## Pós-instalação

Recarregar a extensão no Chrome e recarregar a aba ChatGPT de origem.

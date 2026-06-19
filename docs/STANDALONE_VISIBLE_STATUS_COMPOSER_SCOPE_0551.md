# AI Bridge Local 0.5.51 - Standalone visible status composer scope

Data: 2026-06-19T13:51:23.247479+00:00

## Problema

A entrega direta inter-chat funcionou, mas o status visivel no chat origem falhou com:

`aiBridgeFindChatGptPromptTextarea is not defined`

A causa era escopo: o scanner standalone usava helper criado fora do IIFE standalone.

## Correcao

- Adiciona helpers de composer dentro do scanner standalone.
- `findComposer()` do standalone passa a usar `aiBridgeStandaloneFindPreferredComposer()`.
- Prioriza `#prompt-textarea.ProseMirror[contenteditable='true']`.
- Ignora inputs de upload/camera.
- Ajusta o smoke para proibir o helper fora de escopo apenas dentro do standalone.
- Mantem entrega direta inter-chat ja funcional.
- Mantem gateway obrigatorio para `run-command/local_capability`.

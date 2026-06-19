# AI Bridge Local 0.5.50 - Repair prompt-textarea composer smoke

Data: 2026-06-19T13:42:47.639435+00:00

## Problema

O patch de composer priorizou `#prompt-textarea`, mas o smoke anterior falhou porque o marcador `composer_descriptor` nao entrou por um padrao rigido demais.

## Correcao

- Completa o patch 0.5.50 mesmo se `VERSION` ja estava parcialmente em 0.5.50.
- Insere `composer_descriptor: aiBridgeDescribeComposerElement(composer)` com busca flexivel.
- Mantem priorizacao explicita de `#prompt-textarea.ProseMirror[contenteditable='true']`.
- Mantem filtros para ignorar inputs de upload/camera.
- Mantem checagem explicita de exit code em comandos nativos.

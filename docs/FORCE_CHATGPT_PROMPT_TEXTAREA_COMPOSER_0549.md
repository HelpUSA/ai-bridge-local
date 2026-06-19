# AI Bridge Local 0.5.49 - Force ChatGPT prompt-textarea composer

Data: 2026-06-19T13:36:26.358557+00:00

## Problema

O diagnostico no chat destino mostrou que o elemento correto aceita texto:

- selector: `#prompt-textarea`
- tag: `DIV`
- role: `textbox`
- contenteditable: `true`
- class: `ProseMirror`
- inserted: `true`

Mesmo assim a rota direta falhava com `composer_empty_after_inject`.

## Correção

- `findComposer()` agora prioriza explicitamente `#prompt-textarea.ProseMirror[contenteditable='true']`.
- Inputs de upload/camera são ignorados.
- Diagnostico de falha inclui descritor do composer escolhido.
- Mantém scanner standalone e rota direta.
- Mantém gateway obrigatório para `run-command/local_capability`.

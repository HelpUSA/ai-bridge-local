# AI Bridge Local 0.5.48 - Robust composer text injection

Data: 2026-06-19T13:23:53.666385+00:00

## Problema

A rota direta chegou ao chat destino, mas falhou com:

`composer_empty_after_inject`

Isso indica que o composer foi encontrado, mas o texto não permaneceu após a tentativa de injeção.

## Correção

- Adiciona `aiBridgeRobustSetText`.
- Usa setter nativo para textarea/input.
- Usa `execCommand`, seleção/range e DOM de parágrafos para contenteditable.
- Dispara eventos `beforeinput`, `input`, `change` e `keyup`.
- Mantém scanner standalone com feedback visível.
- Mantém gateway obrigatório para `run-command/local_capability`.

## Segurança

A trava contra sobrescrever texto manual diferente permanece.

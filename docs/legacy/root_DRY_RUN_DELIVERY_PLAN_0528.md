# Dry-run delivery plan 0.5.28

Objetivo: gerar plano readonly de entrega sem enviar mensagem.

## Escopo

- Usa o preflight readonly.
- Gera lista de acoes previstas.
- Mostra alvo, command_id, tamanho de payload e risco.
- Nunca envia mensagens.
- Nunca altera fila.
- Nunca clica em UI.
- Nunca executa entrega inter-chat.

## Arquivo principal

- scripts/watcher/dry_run_delivery_plan.py
# Delivery diagnostic summary 0.5.24

Objetivo: criar resumo local readonly de diagnosticos de entrega.

## Escopo

- Recebe eventos/resultados existentes.
- Classifica com o adaptador readonly.
- Agrupa por tipo de falha.
- Agrupa por status.
- Renderiza resumo textual.
- Nao envia mensagens.
- Nao altera fila.
- Nao executa entrega inter-chat.

## Arquivo principal

- scripts/watcher/delivery_diagnostic_summary.py
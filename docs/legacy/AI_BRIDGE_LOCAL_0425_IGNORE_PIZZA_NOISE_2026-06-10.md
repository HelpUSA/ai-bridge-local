# AI Bridge Local 0.4.25 - filtered reports ignore Pizza noise

Data: 2026-06-10

## Objetivo

A frente 0.4.25 corrige os relatorios filtrados e o health rapido para ignorar comandos do outro chat do projeto Pizza que entraram com prefixo `ai_bridge_local_pizza_`.

## Problema observado

O filtro anterior usava apenas `command_id like ai_bridge_local_%`. Isso ainda incluia comandos do outro chat quando eles usavam IDs como `ai_bridge_local_pizza_*`.

## Correção

Os scripts passam a excluir explicitamente o prefixo:

`ai_bridge_local_pizza_`

Arquivos ajustados:

- `scripts/watcher/ai_bridge_local_filtered_db_status.py`
- `scripts/watcher/ai_bridge_local_health.py`

## Validação esperada

O health deve mostrar o filtro ativo:

`DB_FILTER|prefix=ai_bridge_local_|exclude_prefix=ai_bridge_local_pizza_`

E os comandos recentes devem deixar de exibir entradas `ai_bridge_local_pizza_*`.

## Observação operacional

O projeto Pizza deve usar fila/banco separados ou, no mínimo, `command_id` sem prefixo `ai_bridge_local_`. Este projeto deve permanecer restrito ao AI Bridge Local em `D:/dev/autocode/ai-bridge-local`.

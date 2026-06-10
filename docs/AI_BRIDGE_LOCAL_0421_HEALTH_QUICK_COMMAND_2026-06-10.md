# AI Bridge Local 0.4.21 - health quick command

Data: 2026-06-10

## Objetivo

A frente 0.4.21 adiciona um comando rápido de saúde operacional para o AI Bridge Local.

## Arquivo adicionado

- `scripts/watcher/ai_bridge_local_health.py`

## O que o comando verifica

- status do git
- últimos commits
- tags `v0.4.*`
- existência de `queue_local.db`
- contagens filtradas por `command_id like ai_bridge_local_%`
- comandos recentes da frente AI Bridge Local
- dry-run de limpeza de `temp/watcher_scripts`
- `git diff --check`

## Uso

```text
python scripts/watcher/ai_bridge_local_health.py
```

## Resultado esperado

O script imprime `HEALTH_RESULT|OK` quando o banco local existe e o `git diff --check` passa.

## Relação com versões anteriores

- 0.4.18 criou utilitários de banco e limpeza.
- 0.4.19 adicionou relatório filtrado por frente.
- 0.4.20 consolidou relatório operacional completo.
- 0.4.21 cria um comando mais curto para checagem rápida.

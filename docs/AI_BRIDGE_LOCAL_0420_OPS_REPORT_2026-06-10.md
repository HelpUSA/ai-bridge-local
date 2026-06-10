# AI Bridge Local 0.4.20 - ops report

Data: 2026-06-10

## Objetivo

A frente 0.4.20 cria um comando operacional padronizado para consultar o estado local do AI Bridge Local sem repetir manualmente diversos scripts.

## Arquivo adicionado

- `scripts/watcher/ai_bridge_local_ops_report.py`

## O que o relatorio executa

- `git status -sb`
- `git log --oneline -12`
- lista de tags `v0.4.*`
- relatorio filtrado por prefixo `ai_bridge_local_`
- relatorio geral do banco local
- dry run de limpeza de `temp/watcher_scripts`
- smoke script 0.4.17
- `git diff --check`

## Uso

Execucao completa:

```text
python scripts/watcher/ai_bridge_local_ops_report.py
```

Execucao sem smoke:

```text
python scripts/watcher/ai_bridge_local_ops_report.py --skip-smoke
```

Alterar quantidade preservada no dry run de limpeza:

```text
python scripts/watcher/ai_bridge_local_ops_report.py --cleanup-keep 50
```

## Observacao

Esta versao nao altera worker, gateway ou extensao. Ela consolida os utilitarios 0.4.18 e 0.4.19 em um unico ponto operacional.

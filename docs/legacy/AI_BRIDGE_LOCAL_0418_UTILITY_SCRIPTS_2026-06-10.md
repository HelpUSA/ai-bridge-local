# AI Bridge Local 0.4.18 - utility scripts

Data: 2026-06-10

## Objetivo

A frente 0.4.18 adiciona utilitarios operacionais para consultar o banco local e controlar a pasta de scripts temporarios criada pelo fluxo script_text.

## Arquivos adicionados

- scripts/watcher/ai_bridge_local_db_status.py
- scripts/watcher/ai_bridge_local_cleanup_watcher_scripts.py

## Utilitario de banco

O script ai_bridge_local_db_status.py imprime contagens por status e os comandos recentes de queue_local.db. Ele serve para auditoria rapida de acked, failed, queued e delivering.

Uso:

python scripts/watcher/ai_bridge_local_db_status.py

## Utilitario de limpeza

O script ai_bridge_local_cleanup_watcher_scripts.py lista e pode remover arquivos antigos de temp/watcher_scripts preservando os N mais recentes.

Modo seguro dry run:

python scripts/watcher/ai_bridge_local_cleanup_watcher_scripts.py --keep 30

Modo efetivo com delecao:

python scripts/watcher/ai_bridge_local_cleanup_watcher_scripts.py --keep 30 --delete

## Validacao

- db status executado com sucesso
- cleanup dry run executado com sucesso
- git diff --check executado antes do commit
- baseline 0.4.17 mantido pela tag v0.4.17-operational-baseline

## Observacao

Esta etapa nao altera o worker nem a extensao. E uma frente operacional incremental sobre a baseline 0.4.17.

# AI Bridge Local - Local bridge store 0.4.65

## Objetivo
Criar base local para inbox, outbox e status, mantendo dry-run como padrao.

## Arquivos
- scripts/watcher/local_bridge_store.py
- scripts/watcher/local_bridge_reconcile.py
- scripts/watcher/smoke_local_bridge_store.py

## Garantias
- Nao executa comandos externos.
- Modo dry-run por padrao.
- Escrita real apenas com --apply e destinada a store-dir controlado.
- Smoke usa diretÃ³rio temporario, sem sujar o repo.

## Proximos passos
- Adicionar schema de envelope entre chats.
- Adicionar replayer dry-run.
- Criar painel local para visualizar inbox/outbox/status.

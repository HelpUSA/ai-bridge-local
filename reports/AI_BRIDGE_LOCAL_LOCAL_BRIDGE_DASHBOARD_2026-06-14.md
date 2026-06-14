# AI Bridge Local - Local bridge dashboard 0.4.68

## Objetivo
Criar painel read-only via CLI para visualizar inbox, outbox e status do local bridge store.

## Arquivos
- scripts/watcher/local_bridge_dashboard.py
- scripts/watcher/local_bridge_dashboard_summary.py
- scripts/watcher/smoke_local_bridge_dashboard.py

## Garantias
- Somente leitura no dashboard.
- Resumo textual para reduzir truncamento.
- Smoke cria store temporario dentro de temp/ e remove ao final.

## Proximos passos
- Criar replay apply controlado.
- Criar worker opcional em dry-run.
- Criar visualizacao HTML/local se necessario.

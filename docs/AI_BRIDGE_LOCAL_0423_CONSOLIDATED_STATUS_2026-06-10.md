# AI Bridge Local - status operacional consolidado 0.4.23

Data: 2026-06-10

## Estado atual

- Branch: main
- Working tree esperado: limpo
- Baseline operacional atual: v0.4.22-cleanup-policy como ultima politica aplicada antes deste consolidado
- Frente 0.4.23: documento consolidado de operacao

## Sequencia fechada

- 0.4.17: visual dedupe, temp script workflow, smoke script e baseline operacional
- 0.4.18: utilitarios de banco e cleanup
- 0.4.19: status de banco filtrado por frente ai_bridge_local_
- 0.4.20: relatorio operacional consolidado
- 0.4.21: health check rapido
- 0.4.22: politica segura de cleanup com token de confirmacao para delete
- 0.4.23: status operacional consolidado

## Scripts operacionais disponiveis

- scripts/watcher/ai_bridge_local_smoke_0417.ps1
- scripts/watcher/ai_bridge_local_db_status.py
- scripts/watcher/ai_bridge_local_cleanup_watcher_scripts.py
- scripts/watcher/ai_bridge_local_filtered_db_status.py
- scripts/watcher/ai_bridge_local_ops_report.py
- scripts/watcher/ai_bridge_local_health.py
- scripts/watcher/ai_bridge_local_cleanup_policy.py

## Comandos recomendados

Health rapido:

python scripts/watcher/ai_bridge_local_health.py

Relatorio operacional sem smoke:

python scripts/watcher/ai_bridge_local_ops_report.py --skip-smoke

Relatorio operacional completo:

python scripts/watcher/ai_bridge_local_ops_report.py

Cleanup seguro em dry-run:

python scripts/watcher/ai_bridge_local_cleanup_policy.py --keep 30

Cleanup efetivo com confirmacao explicita:

python scripts/watcher/ai_bridge_local_cleanup_policy.py --keep 30 --delete --confirm AI_BRIDGE_LOCAL_DELETE_TEMP_SCRIPTS

## Status git capturado

## main

## Log recente

c189b4a Add AI Bridge Local 0.4.22 cleanup policy
d1a4276 Add AI Bridge Local 0.4.21 health command
4bcdd28 Add AI Bridge Local 0.4.20 ops report
c428d0d Add AI Bridge Local 0.4.19 filtered DB status
94da4fe Document AI Bridge Local 0.4.18 utility scripts
b44ba48 Add AI Bridge Local 0.4.18 utility scripts
7d33042 Add AI Bridge Local 0.4.17 smoke script
9c50b16 Document AI Bridge Local current status 0.4.17
e47184e Add AI Bridge Local visual dedupe and temp scripts 0.4.17
43b61d5 Add AI Bridge Local submit recovery 0.4.16
e2d0e3e Document AI Bridge Local baseline and command usage
6262cde Confirm ChatGPT send before ACK in AI Bridge Local 0.4.14
a25073e Stabilize AI Bridge Local 0.4.13 and run-command 0.2.1
12acc6a Add local run-command smoke checker
2786c2b Initialize AI Bridge Local interchat baseline

## Tags atuais


## Observacoes

- O repositorio local continua sem remoto/origin configurado, salvo alteracao manual externa.
- O banco queue_local.db pode conter comandos de outras frentes; use o relatorio filtrado para AI Bridge Local.
- O health check atual retornou OK antes da criacao deste documento.

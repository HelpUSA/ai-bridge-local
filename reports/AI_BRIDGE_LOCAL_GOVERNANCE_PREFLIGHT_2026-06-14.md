# AI Bridge Local - Governance preflight 0.4.73

## Objetivo
Criar preflight read-only que usa o governance_risk_classifier para emitir avisos antes de comandos watcher.

## Arquivos
- scripts/watcher/governance_preflight.py
- scripts/watcher/smoke_governance_preflight.py

## Garantias
- Nao executa o comando analisado.
- Nao bloqueia automaticamente.
- Emite warnings para mutating, destructive e unknown_review_required.
- Pode ser integrado ao fluxo de montagem de envelopes em etapa futura.

## Proximo passo
Integrar governance_preflight ao command_builder ou criar gate opcional para watcher apply.

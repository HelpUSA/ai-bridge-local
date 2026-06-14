# AI Bridge Local - Governance risk classifier 0.4.72

## Objetivo
Criar classificador read-only de risco para comandos watcher antes de futuros apply.

## Arquivos
- scripts/watcher/governance_risk_classifier.py
- scripts/watcher/smoke_governance_risk_classifier.py

## Classes
- read_only_or_dry_run
- mutating
- destructive
- unknown_review_required
- empty

## Garantias
- Nao executa o comando analisado.
- Apenas classifica texto.
- Pode ser integrado no preflight antes de releases futuras.

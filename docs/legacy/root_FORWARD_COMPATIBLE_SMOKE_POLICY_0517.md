# Forward-compatible smoke policy 0.5.17

Objetivo: impedir que smokes historicos quebrem versoes futuras por comparacao rigida de VERSION.

## Problema resolvido

Smokes dos micros 0.5.14 e 0.5.15 falharam ao evoluir para versoes seguintes porque exigiam VERSION exatamente igual ao micro original.
A politica correta para smokes historicos e validar que a versao atual e igual ou superior ao micro que introduziu a garantia.

## Regra operacional

- Smokes historicos devem usar comparacao de versao minima.
- Somente o smoke do micro atual deve exigir VERSION exatamente igual ao micro atual.
- Todo novo micro deve, quando necessario, tornar o smoke do micro anterior forward-compatible.
- Scripts PowerShell interativos nao devem usar comando que encerra o shell.
- Este micro nao executa entrega inter-chat.

## Arquivo principal

- scripts/watcher/smoke_forward_compatible_smoke_policy_0517.py
# AI Bridge Local - Command builder advisory metadata 0.4.77

## Objetivo
Criar builder advisory compatÃ­vel com envelope local e anexar governance_advisory sem bloquear execucao.

## Arquivos
- scripts/watcher/command_builder_advisory.py
- scripts/watcher/smoke_command_builder_advisory.py

## Garantias
- command_builder original permanece compatÃ­vel e intocado nesta etapa.
- O wrapper monta envelope local compatÃ­vel e anexa governance_advisory.
- governance_advisory vem de governance_preflight.py.
- O comportamento e nao bloqueante: blocks_execution permanece False.

## Proximo passo
Criar gate opcional por flag para recusar destructive apenas quando explicitamente habilitado.

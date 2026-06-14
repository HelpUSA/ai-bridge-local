# AI Bridge Local - Command builder governance 0.4.74

## Objetivo
Integrar governance_preflight ao command_builder como aviso estruturado e nao bloqueante.

## Arquivos
- scripts/watcher/command_builder.py
- scripts/watcher/smoke_command_builder_governance.py

## Garantias
- Integracao exposta por governance_preflight_for_command.
- Nao executa o comando analisado.
- Nao bloqueia automaticamente.
- Retorna schema ai_bridge_local.governance_preflight com risk_level, warnings e requires_manual_review.

## Proximo passo
Usar o retorno de governance_preflight_for_command na montagem dos envelopes locais para mostrar risco antes do envio.

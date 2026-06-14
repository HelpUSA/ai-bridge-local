# AI Bridge Local - Command builder advisory gate 0.4.78

## Objetivo
Criar gate opcional por flag para command_builder_advisory, sem alterar o comportamento padrao.

## Garantias
- Sem bloqueio padrao.
- --fail-on-destructive bloqueia destructive apenas quando solicitado.
- --fail-on-mutating bloqueia mutating e destructive apenas quando solicitado.

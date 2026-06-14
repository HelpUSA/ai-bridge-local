# AI Bridge Local - Governance roadmap 0.4.76

## Objetivo
Consolidar a camada de governanca criada entre 0.4.72 e 0.4.75 e definir proximos passos seguros.

## Estado consolidado
- 0.4.72: governance_risk_classifier.py classifica risco sem executar comandos.
- 0.4.73: governance_preflight.py emite warnings read-only e nao bloqueantes.
- 0.4.74: command_builder.py recebeu helper governance_preflight_for_command.
- 0.4.75: tag final de rastreabilidade criada no HEAD correto.

## Garantias atuais
- Nenhum comando analisado e executado pela governanca.
- Nenhum gate bloqueante foi ativado automaticamente.
- O fluxo permanece compatÃ­vel com envelopes locais existentes.
- Smokes cobrem read-only, mutating, destructive e alinhamento de versao.

## Roadmap recomendado
1. Criar modo advisory no command_builder para anexar risk_level ao envelope gerado.
2. Criar gate opcional por flag para recusar destructive sem allow explÃ­cito.
3. Registrar decisÃµes de risco em relatÃ³rio local antes de apply.
4. SÃ³ depois considerar enforcement padrÃ£o.

## Fora de escopo nesta release
- Nao bloquear comandos automaticamente.
- Nao alterar semantica de execucao do watcher.
- Nao mover tags antigas.

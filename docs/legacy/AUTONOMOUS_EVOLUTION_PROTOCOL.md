# AI Bridge Local - Autonomous evolution protocol 0.4.92

## Objetivo
Definir protocolo seguro para a IA propor, simular, aplicar e auditar evolucao do repo via watcher.

## Fluxo obrigatorio
1. Descobrir estado atual com comandos read-only.
2. Criar proposta pequena e reversivel.
3. Classificar risco com governance dry-run.
4. Gerar plano de mudanca sem executar destruicao.
5. Aplicar em bloco pequeno quando aprovado.
6. Rodar smoke especifico e smoke_docs.
7. Rodar release_check.
8. Commitar, taguear e fazer push.
9. Rodar audit final read-only.

## Guardrails
- Sem alteracao destrutiva implicita.
- Sem limpeza de fila sem snapshot e aprovacao explicita.
- Sem mudanca global de enforcement sem dry-run e release dedicado.
- Sem comandos grandes repetidos depois de parse error.
- Python com indentacao sensivel deve usar Base64.

## Resultado esperado
A IA pode evoluir o repo por ciclos pequenos, rastreaveis e auditados, mantendo rollback e seguranca operacional.

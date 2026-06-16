# AI Bridge Local - Self evolution guardrails 0.4.90

## Objetivo
Definir guardrails para evolucao assistida ou autonoma do repo usando watcher.

## Principios obrigatorios
- Comecar por leitura e diagnostico.
- Propor plano antes de alterar runtime, banco, credenciais ou deploy.
- Preferir dry-run para comandos mutating e destructive.
- Dividir alteracoes em releases pequenos.
- Rodar smoke especifico antes de commit.
- Rodar release_check antes de tag e push.
- Rodar audit final read-only apos push.
- Nunca expor segredos em logs, docs ou commits.
- Nunca limpar fila, banco ou artefatos sem snapshot e autorizacao explicita.

## Fluxo seguro de evolucao
1. Inspecionar estado do repo.
2. Classificar risco da mudanca.
3. Criar patch pequeno.
4. Rodar smokes locais.
5. Atualizar docs e VERSION.
6. Commitar, taguear e publicar.
7. Auditar alinhamento final.

# AI Bridge Local - Autonomous evolution approval matrix 0.4.93

## Objetivo
Definir quando a IA pode propor, executar, pausar ou exigir aprovacao explicita durante evolucao autonoma.

## Matriz de aprovacao
- read_only: permitido para diagnostico, auditoria e verificacao.
- docs_only: permitido com smoke especifico, smoke_docs, version_alignment e audit final.
- low_risk_code: permitido somente em release dedicada com diff pequeno e rollback claro.
- mutating_runtime: exige plano, dry-run, release_check e aprovacao explicita.
- data_cleanup: exige snapshot, plano dry-run e aprovacao explicita.
- destructive: bloqueado por padrao, exceto com aprovacao explicita e escopo minimo.

## Regras de parada
- Parar ao encontrar falha de smoke.
- Parar ao encontrar divergencia entre VERSION, manifest, guia e tag.
- Parar se git diff --check falhar.
- Parar se a mudanca tocar segredos, credenciais ou dados sensiveis.

## Resultado esperado
A evolucao autonoma fica limitada por risco, aprovacao, auditabilidade e reversibilidade.

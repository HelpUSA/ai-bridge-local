# AI Bridge Local - Autonomous change proposal template 0.4.94

## Objetivo
Padronizar a proposta que a IA deve produzir antes de qualquer mudanca autonoma no repo via watcher.

## Template obrigatorio
- Contexto atual: estado do repo, versao, branch, tag e smokes relevantes.
- Problema: qual lacuna sera corrigida.
- Escopo: arquivos previstos e tipo de mudanca.
- Risco: read_only, docs_only, low_risk_code, mutating_runtime, data_cleanup ou destructive.
- Plano dry-run: comandos de verificacao sem efeito colateral.
- Plano de aplicacao: bloco pequeno e reversivel.
- Plano de teste: smoke especifico, smoke_docs, smoke_version_alignment e release_check.
- Rollback: como desfazer a mudanca.
- Audit final: HEAD, tag, VERSION, guia, smokes e git diff --check.

## Regras
- Toda proposta deve caber em uma release pequena.
- Mudancas destrutivas exigem aprovacao explicita.
- Mudancas em dados exigem snapshot e plano dry-run.
- Mudancas em codigo exigem teste minimo e rollback claro.

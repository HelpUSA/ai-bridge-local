---
type: operations
status: draft
tags:
  - operations
  - rollback
---

# Rollback

## Principio

Rollback deve retornar ao ultimo commit/tag validado.

## Checklist

- identificar tag valida
- revisar git status
- criar backup se houver alteracoes locais
- reverter com git revert ou reset controlado
- rodar smokes minimos

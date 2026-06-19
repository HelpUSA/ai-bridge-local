---
type: operations
status: draft
tags:
  - operations
  - release
---

# Release process

## Ordem

1. git status limpo ou mudancas conhecidas.
2. aplicar patch pequeno.
3. node --check quando houver JS.
4. smokes especificos.
5. git diff --check.
6. commit.
7. tag.
8. push.

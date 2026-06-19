# AI Bridge Local 0.5.40 - Gemini manifest name sync

Data: 2026-06-19T01:23:21.825870+00:00

## Objetivo

Sincronizar o nome visível da extensão Chrome com a versão declarada.

## Mudança

- `VERSION`: `0.5.39` -> `0.5.40`
- `extension/manifest.json.version`: `0.5.40`
- `extension/manifest.json.name`: `AI Bridge Local 0.5.40`

## Motivo

O diagnóstico do Gemini watcher mostrou `version=0.5.39`, mas `name=AI Bridge Local 0.5.38`.
Isso pode causar confusão ao recarregar/verificar a extensão no Chrome.

## Observação

Não houve alteração funcional na entrega Gemini neste patch.

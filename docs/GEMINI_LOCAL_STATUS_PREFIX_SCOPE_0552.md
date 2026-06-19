# AI Bridge Local 0.5.52 - Gemini local status prefix scope

Data: 2026-06-19T14:11:40.635324+00:00

## Problema

O Gemini envelope observer quebrava com:

`LOCAL_STATUS_PREFIXES is not defined`

## Correcao

- Define `LOCAL_STATUS_PREFIXES` no topo do content script.
- Publica tambem:
  - `globalThis.__AI_BRIDGE_LOCAL_STATUS_PREFIXES__`
  - `window.__AI_BRIDGE_LOCAL_STATUS_PREFIXES__`
- Preserva os prefixos:
  - `[AI_LOCAL_ERRO]`
  - `[AI_LOCAL_RUN]`
  - `[AI_LOCAL]`
- Remove a dependencia de escopo local para o observer do Gemini.
- Mantem rota direta inter-chat sem gateway/DB.
- Mantem gateway obrigatorio para `run-command/local_capability`.

## Validacao esperada

Depois de recarregar a extensao e o Gemini, o console nao deve mais mostrar:

`ReferenceError: LOCAL_STATUS_PREFIXES is not defined`

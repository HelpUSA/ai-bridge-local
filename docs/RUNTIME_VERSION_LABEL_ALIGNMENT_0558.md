# Runtime version label alignment 0.5.58

Data: 2026-06-19T12:39:40.557740

## Objetivo

Remover labels antigos como versao=0.5.52 de recibos e logs emitidos pelos arquivos runtime da extensao.

## Problema observado

Mesmo apos correcoes recentes, alguns recibos [AI_LOCAL] ainda exibiam versao=0.5.52. Isso confundia a leitura operacional, apesar da entrega direta estar funcionando.

## Correcao

A 0.5.58 alinha VERSION, manifest, CAPTURE_VERSION e strings runtime antigas nos arquivos:

- extension/content_script.js
- extension/background.js

## Validacao

- node --check extension/content_script.js
- node --check extension/background.js
- smoke_runtime_version_label_alignment_0558.py
- git diff --check

## Observacao

Docs e reports historicos nao foram limpos por este patch. A limpeza e apenas no runtime da extensao.

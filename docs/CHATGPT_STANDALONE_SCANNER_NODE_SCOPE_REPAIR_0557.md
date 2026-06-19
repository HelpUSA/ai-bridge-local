# ChatGPT standalone scanner node scope repair 0.5.57

Data: 2026-06-19T12:30:06.053507

## Objetivo

Corrigir erro no console do ChatGPT origem:

Uncaught ReferenceError: node is not defined
at scan (content_script.js:2165)

## Causa

O scanner standalone antigo chamava:

processText(text, reason, bootstrapOnly, node);

mas a variavel node nao existe naquele escopo. Isso quebrava o scan e impedia/atrapalhava a captura do envelope outbound.

## Correcao

A chamada foi alterada para:

processText(text, reason, bootstrapOnly, null);

Tambem foram atualizados labels antigos [Local v0.5.52] para [Local v0.5.57] para reduzir confusao operacional.

## Validacao

- node --check extension/content_script.js
- node --check extension/background.js
- smoke_chatgpt_standalone_scanner_node_scope_0557.py
- git diff --check

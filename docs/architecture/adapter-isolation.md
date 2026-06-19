---
type: explanation
status: draft
tags:
  - architecture
  - adapters
---

# Adapter isolation

## Problema

Mudancas no codigo do ChatGPT podem quebrar Gemini, DeepSeek ou HelpUSAI quando os adapters estao acoplados.

## Solucao

Cada IA deve ter adapter proprio com contrato e smokes especificos.

## Regra

Mudanca em um adapter nao deve alterar codigo dos outros adapters.

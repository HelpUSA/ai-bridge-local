---
type: reference
status: draft
tags:
  - reference
  - adapters
  - contract
---

# Adapter contract

Cada IA deve ter adapter isolado.

## Adapters atuais

- ChatGPT
- Gemini
- DeepSeek
- HelpUSAI

## Interface esperada

- detectPage
- getChatId
- findComposer
- injectText
- clickSend
- captureOutboundEnvelope
- showReceipt

## Regra de isolamento

Mudanca em um adapter nao pode alterar codigo dos outros adapters.

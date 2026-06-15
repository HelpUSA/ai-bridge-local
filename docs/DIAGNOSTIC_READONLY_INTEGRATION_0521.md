# Diagnostic classifier readonly integration 0.5.21

Objetivo: integrar o classificador de diagnostico em um adaptador readonly para eventos/resultados existentes.

## Escopo

- Nao envia mensagens.
- Nao altera fila.
- Nao clica em UI.
- Nao executa entrega inter-chat.
- Apenas classifica textos ja existentes em objetos diagnosticos.

## Arquivo principal

- scripts/watcher/delivery_diagnostic_integration.py
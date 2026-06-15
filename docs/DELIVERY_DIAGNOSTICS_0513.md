# Delivery diagnostic classifier 0.5.13

Objetivo: adicionar um classificador local, puro e readonly para transformar textos de erro de entrega em codigos estaveis de diagnostico.

## Escopo

Este micro nao executa entrega inter-chat.
Este micro nao altera o fluxo real de injecao/envio.
Este micro cria uma base reutilizavel para evoluir diagnostico sem depender de testes manuais entre chats.

## Codigos cobertos

- target_chat_not_registered
- target_tab_not_open
- composer_not_found
- modal_blocking
- send_button_disabled
- inject_timeout
- submit_not_confirmed
- delivery_not_acked
- unknown_delivery_failure

## Arquivos principais

- scripts/watcher/delivery_diagnostic_classifier.py
- scripts/watcher/smoke_delivery_diagnostic_classifier_0513.py

## Proxima evolucao sugerida

Integrar o classificador nos pontos que geram AI_LOCAL_ERRO e delivery_result, mantendo primeiro modo readonly/smoke antes de alterar envio real.

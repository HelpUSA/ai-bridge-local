# Delivery failure fixtures 0.5.23

Objetivo: criar fixtures estaticas para validar o diagnostico readonly de falhas conhecidas.

## Cobertura

- submit_not_confirmed
- modal_blocking
- send_button_disabled
- composer_not_found
- target_chat_not_registered
- target_tab_not_open
- delivery_not_acked
- inject_timeout
- unknown_delivery_failure

## Escopo

As fixtures sao dados estaticos.
As fixtures nao enviam mensagens.
As fixtures nao alteram fila.
As fixtures nao executam entrega inter-chat.
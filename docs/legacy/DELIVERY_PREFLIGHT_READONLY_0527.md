# Delivery preflight readonly 0.5.27

Objetivo: criar preflight readonly obrigatorio antes de qualquer entrega real.

## Checks

- target_chat_id
- target_registered
- target_tab_open
- composer_available
- composer_empty
- send_button_enabled
- no_blocking_modal
- source_target_distinct
- payload_present
- manual_authorization

## Escopo

O preflight apenas avalia snapshot existente.
Ele nao envia mensagens.
Ele nao altera fila.
Ele nao clica em UI.
Ele nao executa entrega inter-chat.
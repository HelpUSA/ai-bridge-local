# Delivery diagnostics 0.5.12

Objetivo: melhorar o diagnostico operacional de falhas de entrega sem executar testes reais entre chats.

## Taxonomia minima

- target_chat_not_registered: destino nao localizado nos registros locais.
- target_tab_not_open: aba destino nao esta aberta ou esta suspensa.
- composer_not_found: campo de composicao nao foi encontrado.
- modal_blocking: modal de compartilhamento ou bloqueio visual impede envio.
- send_button_disabled: botao de envio nao esta disponivel.
- inject_timeout: timeout generico apos tentativa de injecao.
- submit_not_confirmed: envio tentado, mas o texto permaneceu no composer.

## Regra operacional

Este micro nao executa entrega inter-chat. Ele apenas documenta a taxonomia e cria smoke readonly para proteger o comportamento esperado.

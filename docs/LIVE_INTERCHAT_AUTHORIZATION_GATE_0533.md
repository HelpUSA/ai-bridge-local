# Live interchat authorization gate 0.5.33

Objetivo: criar uma trava readonly formal antes de qualquer teste real inter-chat.

## Requisitos

- authorization precisa ser exatamente I_AUTHORIZE_REAL_INTERCHAT_SMOKE.
- payload precisa conter [AI_BRIDGE_LIVE_SMOKE].
- source_chat_id precisa existir.
- target_chat_id precisa existir.
- source e target precisam ser diferentes.
- dry_run_passed precisa ser verdadeiro.
- preflight_allowed precisa ser verdadeiro.
- repo_clean precisa ser verdadeiro.
- manual_operator_present precisa ser verdadeiro.

## Escopo

Este micro apenas avalia autorizacao.
Este micro nao envia mensagens.
Este micro nao altera fila.
Este micro nao clica em UI.
Este micro nao executa entrega inter-chat.

## Proximo passo

Depois deste gate, o teste real deve ser outro release isolado, com destino e payload revisados manualmente.
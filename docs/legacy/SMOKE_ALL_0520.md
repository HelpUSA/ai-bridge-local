# Smoke all 0.5.20

Objetivo: criar um agregador local para executar smokes seguros do diretorio scripts/watcher em ordem previsivel.

## Arquivo principal

- scripts/watcher/smoke_all.py

## Escopo

O agregador executa smokes locais e readonly.
Ele nao executa entrega inter-chat.
Ele pula smokes legados explicitamente marcados como incompativeis com o agregador geral.
Ele reduz erro operacional ao substituir listas longas de comandos por um ponto unico de validacao.

## Smokes legados pulados

- smoke_command_accepted_progress_notice.py
- smoke_composer_submit_guard.py
- smoke_disable_worker_running_notice.py
- smoke_gateway_feedback_dedup.py
- smoke_rollback_helper.py
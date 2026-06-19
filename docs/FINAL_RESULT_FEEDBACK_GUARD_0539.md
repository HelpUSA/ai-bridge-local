# AI Bridge Local 0.5.39 - final result feedback guard

Data: 2026-06-19T01:12:11.721910+00:00

## Objetivo

Impedir que o gateway gere feedback local intermediario para mensagens de resultado final.

## Problema observado

Quando o worker enfileira um resultado final como `result_to_<command_id>`, o gateway podia gerar tambem linhas `local_status_accepted_result_to_*`.

Essas linhas internas nao sao o resultado final real. Elas podiam ficar queued/delivering/failed e causar ruido, loops, reentrega antiga ou falsa impressao de que o `[AI_LOCAL_RUN]` final nao chegou.

## Correção

`gateway_local.py` agora possui:

- `is_final_result_feedback_notice(body)`
- `should_skip_source_feedback(body)`

A funcao `enqueue_source_feedback(...)` retorna sem gerar feedback quando o comando é:

- `local_status_*`
- `result_to_*`
- mensagem com `[AI_LOCAL_RUN]`
- mensagem com `result_is_final=1` e `chat_can_continue=...`

## Regra operacional

O fluxo esperado continua sendo:

1. feedback inicial de fila/queued;
2. resultado final real via `[AI_LOCAL_RUN]`.

O resultado final real permanece vindo de `brain_worker.py` por `enqueue_result_message(...)`.

## Mitigação temporária

`scripts/watcher/final_result_sweeper_v3.py` pode ser usado temporariamente para recuperar resultados finais recentes presos.

Nao usar v1/v2 em loop contínuo.

## Validação esperada

- `node --check extension/background.js`
- `node --check extension/content_script.js`
- `python -m py_compile gateway_local.py brain_worker.py`
- `python -m py_compile scripts/watcher/final_result_sweeper_v3.py`
- `git diff --check`
- `scripts/watcher/verify_final_result_queue.py`

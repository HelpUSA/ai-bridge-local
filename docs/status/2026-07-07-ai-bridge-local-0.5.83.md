# AI Bridge Local 0.5.83 - Runtime version alignment

Data: 2026-07-07

## Objetivo

Alinhar os labels de runtime depois da extensao chegar a 0.5.82, removendo referencias antigas 0.5.80 e 0.5.81 em gateway, worker e adapter.

## Alteracoes

- VERSION atualizado para 0.5.83.
- gateway_local.py atualizado para 0.5.83.
- brain_worker.py atualizado para 0.5.83.
- queue_adapter.py docstring atualizada para 0.5.83.
- Extensao alinhada para 0.5.83.
- Guia operacional passa a declarar a versao operacional atual 0.5.83.

## Validacao

- python -m py_compile gateway_local.py brain_worker.py queue_adapter.py
- python scripts/watcher/smoke_version_alignment.py
- python scripts/watcher/smoke_0580_browser_actions_queue_adapter.py
- python scripts/watcher/smoke_0581_worker_supervisor.py
- python scripts/watcher/smoke_0582_post_push_audit.py
- git diff --check

## Observacao operacional

O gateway em execucao precisa ser reiniciado para /health e /control/status passarem a reportar 0.5.83.


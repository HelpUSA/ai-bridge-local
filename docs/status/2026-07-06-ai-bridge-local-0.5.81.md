# AI Bridge Local 0.5.81 - Worker Supervisor

Data: 2026-07-06

## Objetivo

Conectar o caminho de polling do brain worker ao executor supervisionado já existente, evitando que run-command seja executado inline dentro de poll_source().

## Alterações

- brain_worker.py versionado como 0.5.81.
- poll_source() agora entrega ações run-command para submit_run_action(action).
- run_action() permanece responsável por cwd lock, execução, resultado e ACK.
- Adicionado heartbeat resiliente do brain_worker via QueueAdapter quando disponível.
- Adicionado smoke scripts/watcher/smoke_0581_worker_supervisor.py.

## Validação

- python -m py_compile brain_worker.py scripts/watcher/smoke_0581_worker_supervisor.py
- python scripts/watcher/smoke_0581_worker_supervisor.py
- git diff --check

## Segurança operacional

- Sem kill de processos.
- Sem alteração no protocolo /bridge/commands, /bridge/next-action ou /bridge/acks.
- Heartbeat falha de forma tolerante se QueueAdapter não estiver disponível.

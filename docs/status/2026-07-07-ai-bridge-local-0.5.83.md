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

<!-- post-release-ops-0583-start -->
## Nota operacional pos-release

Depois do push da 0.5.83, a extensao e os arquivos de runtime foram alinhados para `0.5.83`.

Pontos importantes observados durante a validacao:

- se o gateway antigo ainda estiver em execucao, `/health`, `/control/status` e eventos intermediarios podem continuar mostrando versao antiga;
- o restart do gateway local ou do Control Center e necessario para carregar o `gateway_local.py` novo;
- erros `envelope_parse_error` vistos depois da release foram causados por JSON invalido no envelope, principalmente por backslash em caminhos Windows e quebras de linha cruas em strings;
- esses erros sao pre-gateway e nao alteram arquivos locais.

Acao documentada: criar `docs/how-to/watcher-json-safe-commands.md` e referenciar o checklist no guia operacional.
<!-- post-release-ops-0583-end -->

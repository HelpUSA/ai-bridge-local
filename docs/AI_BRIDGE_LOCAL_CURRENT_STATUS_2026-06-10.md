# AI Bridge Local - status atual 2026-06-10

## Baseline atual

- Versao: 0.4.17
- Commit: e47184e
- Tag: v0.4.17-visual-dedupe-temp-script
- Branch: main
- Worker: brain_worker.py 0.1.3
- Gateway: gateway_local.py mantido
- Repositorio local sem remote/origin configurado

## Validacoes

- git diff --check: OK
- node --check background.js: OK
- node --check content_script.js: OK
- python -m py_compile gateway_local.py brain_worker.py: OK
- run-command tradicional: OK
- temp-script workflow: OK
- cross-profile send-chat-message: acked/button_click_confirmed

## Mudancas 0.4.17

- Visual-dedupe de status compacto local com command_id estavel.
- Temp-script workflow via script_text + script_ext em temp/watcher_scripts.
- Compatibilidade mantida com payload.command tradicional.

## Baselines preservados

- 0.4.16: 43b61d5 / v0.4.16-submit-recovery
- 0.4.14: 6262cde / v0.4.14-confirm-send-before-ack

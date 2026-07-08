# Watcher JSON-safe commands

Data: 2026-07-07
Contexto: AI Bridge Local 0.5.83

## Objetivo

Padronizar como enviar comandos pelo watcher sem quebrar o envelope JSON antes do gateway.

## Regra principal

O bloco entre `@@AI_BRIDGE_LOCAL_START@@` e `@@AI_BRIDGE_LOCAL_END@@` precisa ser JSON estrito. Se o envelope falhar com `envelope_parse_error`, nada foi executado no runner local.

## Regras obrigatorias

- Use sempre `command_id` novo em cada retry.
- Use `source_chat_id` igual ao chat atual.
- Nao use caminhos Windows com barra invertida crua dentro do JSON.
- Prefira caminhos com barra normal: `docs/status`, `scripts/watcher`, `extension/manifest.json`.
- Evite comandos longos inline em PowerShell ou cmd.
- Para comandos com aspas internas, multiline, listas ou textos grandes, use `python -c` com `base64`.
- Nao coloque quebras de linha cruas dentro de strings JSON.
- Trate `AI_LOCAL status=queued` como evento intermediario.
- Aguarde `AI_LOCAL_RUN` final para analisar `stdout`, `stderr` e `return_code`.

## Exemplos de caminhos

Errado dentro do JSON:

```text
docs\status
scripts\watcher
```

Certo dentro do JSON:

```text
docs/status
scripts/watcher
```

## Significado dos eventos

### `AI_LOCAL status=queued`

O comando entrou na fila. Ainda nao ha resultado de execucao.

### `AI_LOCAL_RUN status=acked return_code=0`

O comando executou com sucesso. Pode prosseguir.

### `AI_LOCAL_RUN status=failed`

O comando executou, mas falhou. Analise `stdout` e `stderr` antes de reenviar.

### `AI_LOCAL_ERRO tipo=envelope_parse_error`

O envelope JSON nem chegou ao gateway. Corrija o envelope, use `command_id` novo e reenvie. Nao assuma que qualquer arquivo foi alterado.

## Procedimento recomendado para comandos grandes

1. Escreva o script Python localmente como texto.
2. Codifique o script em base64.
3. Envie um envelope curto com:

```text
python -c "import base64;exec(base64.b64decode('...'))"
```

4. Dentro do script, use `subprocess.run([...])` com listas de argumentos.
5. Imprima marcadores `START` e `END`.
6. Imprima `RC=<codigo>` apos cada validacao importante.

## Checklist seguro para patch

- Confirmar `git status -sb`.
- Abortar se houver dirty worktree inesperado.
- Aplicar patch pequeno.
- Rodar `git diff --check`.
- Rodar os smokes relevantes.
- Fazer commit.
- Fazer push.
- Rodar auditoria pos-push.

## Checklist pos-release

Depois de uma release que altera gateway, worker ou extensao:

1. Confirmar commit e push.
2. Rodar `python scripts/watcher/post_push_audit_0582.py`.
3. Recarregar a extensao no Chrome.
4. Reiniciar gateway local ou Control Center.
5. Confirmar `/health` e `/control/status`.
6. Confirmar se eventos novos mostram a versao esperada.

## Observacao da 0.5.83

Na 0.5.83, o codigo foi alinhado para reportar `0.5.83`, mas o runtime em execucao so muda depois de reiniciar o gateway ou Control Center. Eventos antigos ou processos ainda vivos podem continuar mostrando versao anterior ate o restart.

<!-- AI_BRIDGE_LOCAL_JSON_SAFE_TOOLING_0584_START -->
## 0.5.84 JSON-safe envelope tooling

Use `scripts/watcher/envelope_json_safe_helper.py` when an envelope contains content that is likely to break hand-written JSON, especially quoted Python snippets, multiline messages, or Windows-style paths.

The helper renders strict one-line JSON between the bridge markers and validates the envelope before printing it.

Example for a local command envelope:

```bash
python scripts/watcher/envelope_json_safe_helper.py --source <source_chat_id> --target gateway-brain-supervisor --action run-command --id <command_id> --cwd D:/dev/autocode/ai-bridge-local --command git status --short
```

Example for an inter-chat message envelope:

```bash
python scripts/watcher/envelope_json_safe_helper.py --source <source_chat_id> --target <target_chat_id> --action send-chat-message --id <command_id> --message "message text" --force-gateway
```

Validation helpers:

```bash
python scripts/smoke/smoke_envelope_json_safety.py
python scripts/watcher/post_push_auditor.py --expect-file scripts/watcher/envelope_json_safe_helper.py --expect-file scripts/smoke/smoke_envelope_json_safety.py --expect-file scripts/watcher/post_push_auditor.py
```

Notes:

- Keep the JSON body between markers on one physical line.
- Prefer forward slashes in paths inside envelopes.
- Do not paste raw multiline JSON into a live bridge envelope.
- Do not paste raw Windows backslashes into hand-written JSON.
<!-- AI_BRIDGE_LOCAL_JSON_SAFE_TOOLING_0584_END -->

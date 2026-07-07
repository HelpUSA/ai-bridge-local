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

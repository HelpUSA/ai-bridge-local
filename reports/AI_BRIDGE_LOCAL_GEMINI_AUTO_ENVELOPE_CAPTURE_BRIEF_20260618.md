# Gemini auto envelope capture - briefing operacional

## Alvo

Gemini URL:
https://gemini.google.com/app/9b406ec6ce0bcea0

target_chat_id:
9b406ec6ce0bcea0

## Estado ja validado

- ChatGPT -> watcher -> Gemini: OK.
- Gemini -> watcher/eco -> ChatGPT: OK em modo manual/loopback.
- Auditoria gemini_safe_agent_readiness_audit_20260618_002:
  - PASS manifest_version_0534
  - PASS manifest_host_gemini
  - PASS manifest_match_gemini
  - PASS background_gemini_prefix
  - PASS content_gemini_url
  - PASS content_register
  - PASS composer_generic
  - PASS send_chat_message
  - FAIL has_run_command

## Problema principal

O Gemini consegue receber mensagens via watcher, mas ainda depende de intervencao manual.

O gargalo e:

- o content_script/background consegue enviar mensagens para o Gemini;
- mas ainda nao ha rotina segura para capturar automaticamente um envelope gerado na resposta do Gemini e reenviar esse envelope ao watcher.

Formato que precisa ser capturado:

@@AI_BRIDGE_LOCAL_START@@
{...json unico...}
@@AI_BRIDGE_LOCAL_END@@

## Implementar no content_script.js

Adicionar rotina com MutationObserver para observar novas mensagens/respostas do assistente.

Regras obrigatorias:

- aceitar somente um JSON entre os marcadores;
- rejeitar texto fora dos marcadores;
- rejeitar mais de um envelope na mesma resposta;
- rejeitar JSON invalido;
- deduplicar por command_id;
- nao capturar texto digitado pelo usuario no composer;
- nao reenviar envelopes antigos ja processados;
- limitar tamanho maximo do envelope;
- registrar evento/erro no console ou telemetry.

Mensagem para background sugerida:

type: AI_BRIDGE_CAPTURED_ENVELOPE
source_chat_id: chat atual
raw_text: texto bruto
envelope: JSON parseado

## Implementar no background.js

Ao receber AI_BRIDGE_CAPTURED_ENVELOPE:

- validar source_chat_id;
- validar target_chat_id obrigatorio;
- validar command_id obrigatorio e novo;
- validar conversation_id obrigatorio;
- validar action permitida;
- permitir send-chat-message por padrao;
- run-command somente com gate explicito;
- payload precisa ser objeto quando action=run-command;
- rejeitar comandos destrutivos.

## Gate readonly para run-command

Permitir inicialmente:

- Get-ChildItem
- dir
- git status
- git diff --name-only
- git diff --stat

Bloquear por padrao:

- Remove-Item
- del
- erase
- rm
- rmdir
- move
- mv
- copy
- cp
- Set-Content
- Add-Content
- Out-File
- git add
- git commit
- git push
- npm install
- pip install
- curl | powershell
- Invoke-Expression
- iex

## Template readonly para listar pasta

Quando usuario pedir para ler/listar pasta:

- se nao informou caminho absoluto, pedir caminho;
- se informou caminho absoluto, gerar envelope run-command readonly;
- listar apenas nome, tamanho, data e modo;
- nao usar recursao por padrao;
- limitar saida;
- nao ler conteudo de arquivos sem confirmacao explicita.

Comando permitido recomendado:

Get-ChildItem -LiteralPath '<PASTA>' -Force |
Select-Object Mode,Length,LastWriteTime,Name |
Format-Table -AutoSize

## Smoke automatico

Criar:

scripts/watcher/smoke_gemini_auto_envelope_roundtrip.py

Validar:

- envelope JSON valido e capturado;
- envelope com texto extra rejeitado;
- envelope duplicado por command_id nao reexecutado;
- run-command destrutivo rejeitado;
- run-command readonly permitido;
- send-chat-message permitido.

## Ordem segura

1. Rodar inspecao readonly do diff.
2. Criar testes/smoke para parser de envelope capturado.
3. Implementar parser isolado no content_script.js.
4. Implementar handler seguro no background.js.
5. Implementar gates para action.
6. Adicionar smoke de roundtrip automatico.
7. Rodar git diff --check e smokes.
8. So depois considerar commit.

## Regra importante

Nao mexer em gateway_local.py sem checar antes:

git status -sb
git diff -- gateway_local.py
git diff -- extension/background.js extension/content_script.js extension/manifest.json

Se houver alteracao pendente em gateway_local.py, preservar.

## Resumo em uma frase

Implementar no Gemini a captura automatica e segura de envelopes AI Bridge, com validacao no background, gate readonly para run-command, dedupe por command_id e smoke de roundtrip automatico, sem mexer em gateway_local.py sem checar diff antes.

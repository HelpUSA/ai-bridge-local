# AI Bridge Local - Robustez contra falhas de comandos

Atualizado em 2026-06-12.

## Estado atual confirmado

- HelpUS AI respondeu corretamente ao operador via AI Bridge Local.
- HelpUS AI aprendeu que send-chat-message serve para conversar com outro chat.
- HelpUS AI aprendeu que run-command com local_capability serve para comandos locais.
- run-command com script_text e script_ext foi validado com retorno SCRIPT_TEXT_PY_OK.
- O parser da extensão aceita envelope em 3 linhas e envelope colapsado em linha única.
- Foi criado scripts/watcher/smoke_robustness.py.
- O smoke atual roda e retorna ROBUSTNESS_SMOKE_OK.
- node --check extension/content_script.js passou.
- git diff --check passou.

## Feito

### Compatibilidade com HelpUS AI

- manifest.json e content_script.js aceitam ai.helpusbr.com.
- Operador consegue enviar mensagens para HelpUS AI.
- HelpUS AI consegue responder ao operador via bridge.
- delivery_kind legado local_inter_agent_message é normalizado para inter_agent_message.

### Parser mais tolerante

- Antes a extensão exigia marcador inicial, JSON e marcador final em 3 linhas reais.
- Agora também aceita envelope local colapsado em linha única.
- Isso reduz falhas quando a UI ou o modelo remove quebras de linha.

### Feedback de erro e auditoria

- Gateway registra invalid_messages.
- Gateway registra dead_letters.
- Falhas de parse retornam orientação para corrigir e reenviar.
- Falhas de delivery e ACK foram documentadas nas versões 0.4.29 a 0.4.31.

### script_text e script_ext

- Gateway valida run-command com command, script_text, script_ext ou script_path.
- Worker possui prepare_temp_script.
- Worker executa script_text py e ps1 via arquivo temporário.
- Teste real com script_text py retornou SCRIPT_TEXT_PY_OK.

### Smoke de robustez

- Criado scripts/watcher/smoke_robustness.py.
- O smoke valida marcadores, regex de envelope em linha única, delivery kinds, invalid_messages, dead_letters e suporte a script_text no worker.
- O smoke atual é offline e não envia mensagens nem executa comandos enfileirados.

### Controle de conflito git

- Quando apareceu .git/index.lock, foi feita verificação de processo git antes de qualquer remoção.
- Um revert acidental foi corrigido com revert do revert, sem force-push.

## Ainda precisa ser feito

### Ampliar o smoke

- Testar fila commands em modo offline ou banco temporário.
- Testar invalid_messages com JSON inválido.
- Testar dead_letters com falha simulada.
- Testar command_id duplicado.
- Testar delivery_kind inválido.
- Testar payload incompleto.
- Testar run-command com retorno diferente de zero.
- Testar timeout.
- Testar script_text ps1.
- Testar script_path.
- Testar cwd inexistente.
- Testar source_chat_id_mismatch.
- Testar composer ocupado.

### Criar health check oficial

Arquivo sugerido: scripts/watcher/health_check.py.

Deve verificar git, lock, processos, versões, fila, invalid messages, dead letters, tamanho do banco, delivering antigos e workers duplicados.

### Criar cleanup dry-run

Arquivo sugerido: scripts/watcher/cleanup_queue_dry_run.py.

Deve listar candidatos antigos ou repetidos sem alterar nada.

### Criar cleanup apply seguro

Arquivo sugerido: scripts/watcher/cleanup_queue_apply.py.

Deve exigir dry-run anterior, lista explícita de IDs, auditoria e mover para dead letters quando aplicável.

### Reconciliar Simple Bridge Mode

Decidir se fica oficial, legado documentado ou removido.

### Reconciliar versões

Alinhar manifest.json, content_script.js, background.js, docs e changelog.

### Atualizar guia principal

Consolidar formato de envelope, inter_agent_message, local_capability, payload.command, script_text, script_ext, script_path, checklist de commit/push, index.lock e composer ocupado.

### Teste operacional pós-reload

Recarregar extensão, F5 no ChatGPT e HelpUS AI, testar envelope em 3 linhas, envelope em linha única e run-command com script_text.

## Ordem recomendada

1. Criar health_check.py.
2. Criar cleanup_queue_dry_run.py.
3. Ampliar smoke_robustness.py.
4. Criar cleanup_queue_apply.py.
5. Atualizar AI_BRIDGE_LOCAL_GUIDE.md.
6. Reconciliar Simple Bridge Mode.
7. Reconciliar versões.
8. Fazer smoke operacional completo após reload da extensão.

## Comandos atuais de validação

- python scripts/watcher/smoke_robustness.py
- node --check extension/content_script.js
- git diff --check
- git status -sb

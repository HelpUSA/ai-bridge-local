# AI Bridge Local - Guia Unificado Operacional e Roadmap

Atualizado em: 2026-06-14
Versao atual: 0.4.45
Branch principal: main
Marco publicado mais recente: v0.4.45-send-chat-message-smoke
Commit de referencia: pendente - Add send-chat-message smoke
Repositorio local: D:/dev/autocode/ai-bridge-local

Este arquivo e o documento operacional ativo e consolidado do AI Bridge Local. Ele substitui os documentos soltos anteriores da pasta docs. Os documentos historicos foram preservados em docs/archive E docs/legacy, mas a fonte ativa de orientacao passa a ser este guia unico.

---

## 1. Objetivo do projeto

O AI Bridge Local e a ponte operacional entre conversas do ChatGPT, um gateway local e repositorios de desenvolvimento na maquina do Wagner. O sistema permite:

1. Enviar mensagens entre chats por envelopes locais.
2. Executar comandos locais de forma controlada em repositorios especificos.
3. Registrar resultados, falhas, dead letters, status de entrega e diagnosticos.
4. Padronizar comandos para reduzir erros de JSON, encoding, shell e path.
5. Dar ao Wagner uma forma auditavel de coordenar varios chats e varios repositorios sem perder contexto.

O projeto deve priorizar seguranca operacional. Toda evolucao precisa manter o repositorio recuperavel, com validacoes antes de commit, tag, push, cleanup ou deploy.

---

## 2. Estado atual validado

Estado validado em 2026-06-14:

- Versao: 0.4.44.
- Branch: main.
- Ultimo commit publicado: be59288 Add intent payload support.
- Ultima tag publicada: v0.4.44-intent-payload.
- Marco anterior: d73bc1c Add command builder output file mode.
- Repo remoto: HelpUSA/ai-bridge-local.
- Release check validado na 0.4.44.
- Smoke de payload.intent validado.
- Push para main e tag v0.4.44-intent-payload concluido.

O repositorio havia sido recuperado com sucesso para o estado estavel 0.4.43 antes da implementacao final do payload.intent. A implementacao final da 0.4.44 foi feita com patch em arquivo real e validada antes de commit e push.

---

## 3. Componentes princiqpais

### 3.1 Extensao/browser adapter

A extensao detecta envelopes no chat, entrega mensagens ou comandos, e publica status como AI_LOCAL, AI_LOCAL_RUN e AI_LOCAL_ERRO. Ela tambem lida com confirmacao via botao quando o envio entre chats exige interacao visual.

Pontos de atencao:

- A aba destino precisa estar aberta e funcional.
- Erro submit_button_not_found_or_disabled indica que o envelope foi aceito, mas a interface do chat alvo nao estava pronta.
- Nesses casos, reenvie com command_id novo apos recarregar ou focar a aba destino.

### 3.2 Gateway local

Arquivo principal: gateway_local.py.

Responsabilidades:

- Validar envelope recebido.
- Exigir campos obrigatorios.
- Validar action, delivery_kind e payload.
- Encaminhar comandos para o worker local.
- Rejeitar comandos malformados antes de execucao.

Na versao 0.4.44, o gateway passou a aceitar payload.intent como alternativa a payload.command, payload.script_text ou payload.script_path em action run-command.

### 3.3 Brain worker

Arquivo princiqpal: brain_worker.py.

Responsabilidades:

- Normalizar comandos.
- Criar scripts temporarios quando payload.script_text for usado.
- Executar comandos locais com cwd e timeout controlados.
- Retornar stdout, stderr e return_code.
- Truncar saidas longas.
- Converter payload.intent em chamada segura para scripts/watcher/command_intake.py.

Na versao 0.4.44, quando payload.intent esta presente e nao ha command/script, o worker monta um comando local para command_intake.py. Se payload.execute_intent for verdadeiro, adiciona --execute. Si timeout_seconds existir, repassa --timeout.

### 3.4 Command intake

Arquivo principal: scripts/watcher/command_intake.py.

Responsabilidades:

- Planejar comandos seguros a partir de intents.
- Classificar risco.
- Validar cwd.
- Validar timeout.
- Bloquear operacoes perigosas sem gates explicitos.
- Gerar plano JSON auditavel.
- Executar intents autorizados quando --execute e permitido.

Intents atuais esperados:

- inspect_repo.
- inspect_docs.
- run_smokes.
- run_release_check.
- diagnose_failure.
- backup_queue.
- cleanup_plan.
- placeholders para intents de escrita, git, push e operacoes destrutivas.

### 3.5 Command builder

Arquivo princiqpal: scripts/watcher/command_builder.py.

Responsabilidades:

- Gerar envelopes watcher padronizados.
- Reduzir erros de JSON manual.
- Validar fluxo com o envelope validator.
- Escrever envelope em arquivo via --output-file desde a versao 0.4.43.

### 3.6 Scripts de validacao

Scripts importantes:

- scripts/watcher/release_check.ps1.
- scripts/watcher/validate_all.ps1.
- scripts/watcher/repo_health.py.
- scripts/watcher/smoke_command_builder.py.
- scripts/watcher/smoke_command_builder_validate.py.
- scripts/watcher/smoke_command_builder_output_file.py.
- scripts/watcher/smoke_command_intake.py.
- scripts/watcher/smoke_command_intake_negative.py.
- scripts/watcher/smoke_intent_payload.py.
- scripts/watcher/smoke_docs.py.
- scripts/watcher/smoke_examples.py.

---

## 4. Protocolo de envelopes

Todo envelope local deve ficar sozinho entre os marcadores:

@@@AI_BRIDGE_LOCAL_START@@
{JSON valido}
@@@AI_BRIDGE_LOCAL_END@@

Nao use bloco markdown para o envelope. Nao escreva texto extra dentro dos marcadores.

### 4.1 Comando local

Modelo:

{
  "command_id": "id_unico",
  "source_chat_id": "chat_origem",
  "target_chat_id": "gateway-brain-supervisor",
  "action": "run-command",
  "delivery_kind": "local_capability",
  "conversation_id": "contexto_operacional",
  "from_agent": "nome do agente",
  "payload": {
    "cwd": "D:/dev/autocode/ai-bridge-local",
    "timeout_seconds": 300,
    "command": ["git", "status", "-sb"]
  }
}

### 4.2 Script local

Use script_text para scripts pequenos. Para scripts grandes, crie um arquivo real em scripts/watcher e execute o arquivo.

Modelo seguro:

{
  "payload": {
    "cwd": "D:/dev/autocode/ai-bridge-local",
    "timeout_seconds": 300,
    "script_ext": "ps1",
    "script_text": "Write-Output 'OK'; git status -sb"
  }
}

### 4.3 Mensagem entre chats

Modelo:

{
  "command_id": "id_unico",
  "source_chat_id": "chat_origem",
  "target_chat_id": "chat_destino",
  "action": "send-chat-message",
  "delivery_kind": "inter_agent_message",
  "conversation_id": "contexto",
  "from_agent": "nome do agente",
  "message": "Mensagem para o outro chat.",
  "payload": {}
}

A mensagem deve ir no campo message no topo do JSON. Nao coloque a mensagem dentro de payload.

### 4.4 Uso de payload.intent

A partir da 0.4.44, comandos locais podem usar intent:

{
  "command_id": "id_unico",
  "source_chat_id": "chat_origem",
  "target_chat_id": "gateway-brain-supervisor",
  "action": "run-command",
  "delivery_kind": "local_capability",
  "conversation_id": "intake",
  "from_agent": "agente",
  "payload": {
    "cwd": "D:/dev/autocode/ai-bridge-local",
    "timeout_seconds": 120,
    "intent": "inspect_repo"
  }
}

Para executar uma intent que suporta execucao:

{
  "payload": {
    "cwd": "D:/dev/autocode/ai-bridge-local",
    "timeout_seconds": 120,
    "intent": "run_smokes",
    "execute_intent": true
  }
}

---

## 5. Regras obrigatorias de seguranca

1. Use command_id novo a cada tentativa.
2. Antes de qualquer alteracao, rode git status -sb.
3. Antes de commit, rode:
   - py_compile nos arquivos Python alterados.
   - smokes relacionados.
   - git diff --check.
   - release_check.ps1 quando a alteracao impactar o repo ai-bridge-local.
4. Nao faca commit com repo quebrado.
5. Nao faca push sem release_check OK em mudancas operacionais.
6. Nao faca delete, cleanup, move em massa ou reset sem primeiro listar o que sera afetado.
7. Em falhas de envelope_parse_error, nada foi executado. Corrija e reenvie com command_id novo.
8. Em return_code diferente de zero, o comando executou e pode ter modificado arquivos antes de falhar. Inspecione git status e trechos relevantes antes de tentar novo patch.
9. Evite JSON manual grande.
10. Evite aspas duplas aninhadas dentro de script_text.
11. Evite backslash de Windows dentro de JSON quando puder usar barra normal.
12. Para patches grandes, salve script real em scripts/watcher.
13. Preserve historico em docs/archive ou docs/legacy; nao apague documentacao sem autorizacao.
14. Para outros chats, fiscalize a resposta e exija evidencias objetivas.

---

## 6. O que ja foi feito

### 6.1 Baseline e recuperacao operacional

Foi estabilizado o fluxo local de envio e execucao de comandos via watcher. Foram tratados casos de:

- parse error de envelope.
- falha por aspas quebradas.
- falha por script_text grande.
- falha por indentacao em Python embutido.
- falha por botao de envio indisponivel no chat destino.
- necessidade de command_id novo a cada reenvio.

A documentacao historica foi preservada e o guia principal foi consolidado.

### 6.2 Versoes e marcos recentes

#### 0.4.39

- Alinhamento de nome/manifest.
- Verificacao de versionamento.
- Preparacao para automacao de versao.

#### 0.4.40

- Automacao de version bump.
- Validacao do fluxo command_builder para envelope_validator.
- Tags publicadas para version automation e builder-validator-flow.

#### 0.4.41

- Criado command_intake.py.
- Criado roadmap de command intake.
- Criado smoke_command_intake.py.
- Integracao basica com release_check e validate_all.

#### 0.4.42

- Adicionada politica de risco do command intake.
- Schema version do intake atualizado.
- Criado smoke negativo para comandos bloqueados.
- Melhor cobertura para read_only, validation, write_file, git_write, network_push e destructive.

#### 0.4.43

- command_builder recebeu --output-file.
- Criado smoke_command_builder_output_file.py.
- Release check validando geracao de arquivo de envelope.
- Tag v0.4.43-builder-output-file publicada.

#### 0.4.44

- Gateway passou a aceitar payload.intent.
- Brain worker passou a converter intent em chamada para command_intake.py.
- Criado smoke_intent_payload.py.
- Release check e validate_all passaram a incluir smoke de intent payload.
- Versao bump para 0.4.44.
- Commit be59288 publicado.
- Tag v0.4.44-intent-payload publicada.

### 6.3 Fiscalizacao de outro chat

Foi enviado ao chat alvo 6a2ebf13-87a8-83e9-b8ec-85138199c259 um treinamento operacional para uso correto do watcher. O primeiro envio falhou por submit_button_not_found_or_disabled, indicando aba destino nao pronta. O reenvio foi aceito com resultado acked.

Regras ensinadas ao outro chat:

- Usar run-command para comandos locais.
- Usar send-chat-message para mensagens entre chats.
- Usar message no topo do JSON em inter_agent_message.
- Usar command_id novo sempre.
- Fazer primeiro passo read-only.
- Nao fazer commit, push, cleanup ou deploy sem validacoes.

---

## 7. Padroes de comando seguros

### 7.1 Inspecao read-only inicial

Use quando entrar em qualquer repo:

git status -sb
git log --oneline -5
git diff --stat

### 7.2 Validacao Python

python -m py_compile arquivo1.py arquivo2.py

### 7.3 Validacao geral do AI Bridge Local

powershell -NoProfile -ExecutionPolicy Bypass -File scripts/watcher/release_check.ps1

### 7.4 Diff check

git diff --check

### 7.5 Commit seguro

Antes do commit:

1. git status -sb.
2. py_compile.
3. smokes relacionados.
4. release_check.ps1.
5. git diff --check.
6. git diff --stat.
7. git add somente arquivos esperados.
8. git commit -m "mensagem clara".
9. git tag se for marco de versao.
10. git push.
11. git push origin tag.
12. git status -sb final.

---

## 8. Falhas conhecidas e como corrigir

### 8.1 envelope_parse_error

Sintoma:

- Erro de JSON antes de executar.
- id_original pode aparecer unknown.
- Mensagem informa JSON invalido ou caracteres escapados.

Causa comum:

- aspas duplas dentro de script_text.
- backslash nao escapado.
- caractere invisivel.
- JSON muito grande.
- markdown envolvendo o envelope.
- quebras de linha malformadas.

Correcao:

- Reenviar com command_id novo.
- Reduzir comando.
- Usar script_ext/script_text simples.
- Para conteudo grande, usar arquivo real ou base64.
- Nao assumir que algo foi executado.

### 8.2 return_code 1

Sintoma:

- AI_LOCAL_RUN com status failed.
- O comando executou.
- Pode ter modificado arquivos antes de falhar.

Correcao:

- Inspecionar git status -sb.
- Inspecionar arquivos alterados.
- Nao aplicar patch novo sem entender estado parcial.
- Recuperar com git restore se o estado ficar quebrado e ainda nao houver commit.

### 8.3 submit_button_not_found_or_disabled

Sintoma:

- Entrega entre chats nao consegue clicar/enviar.

Correcao:

- Verificar se aba destino esta aberta.
- Recarregar extensao ou chat.
- Reenviar com command_id novo.
- Manter mensagem curta.

### 8.4 IndentationError em Python

Sintoma:

- Python gerado por script_text perde indentacao ou fica inconsistente.

Correcao:

- Nao montar Python complexo diretamente em script_text.
- Gerar arquivo real.
- Usar base64 para conteudo grande.
- Validar com py_compile antes de smokes.

### 8.5 ModuleNotFoundError em smoke dentro de scripts/watcher

Sintoma:

- Smoke em scripts/watcher nao encontra modulo da raiz.

Correcao:

Adicionar no smoke:

from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd()))

---

## 9. Roadmap detalhado de atividades pendentes

### 9.1 Curto prazo - confiabilidade do watcher

1. Criar smoke especifico para send-chat-message. [DONE 0.4.45 - send-chat-message smoke dedicated]
   - Validar schema.
   - Validar message no topo.
   - Validar payload opcional vazio.
   - Simular erro de destino ausente.
   - Documentar saidas esperadas.

2. Melhorar diagnostico de submit_button_not_found_or_disabled.
   - Capturar se aba destino existe.
   - Capturar se textarea/input foi encontrado.
   - Diferenciar botao desabilitado de seletor inexistente.
   - Sugerir acao objetiva no erro.

3. Criar comando read-only de estado completo.
   - Deve imprimir versao, head, tags recentes, status, release_check resumido.
   - Deve ser seguro para qualquer momento.
   - Pode virar intent inspect_full.

4. Adicionar intent validate_release.
   - Planeja release_check.
   - Executa release_check apenas com execute_intent true.
   - Retorna JSON com status.

5. Adicionar intent inspect_delivery_failure.
   - Recebe command_id.
   - Consulta banco local.
   - Mostra status, dead letter e erro.
   - Nao modifica estado.

### 9.2 Curto prazo - command intake

1. Completar catalogo de intents.
   - inspect_repo.
   - inspect_docs.
   - inspect_file.
   - inspect_diff.
   - run_smokes.
   - run_release_check.
   - diagnose_failure.
   - backup_queue.
   - cleanup_plan.
   - build_envelope.
   - validate_envelope.
   - prepare_patch.
   - apply_patch_file.
   - commit_release.
   - tag_release.
   - push_release.

2. Definir schema de entrada por intent.
   - Campos obrigatorios.
   - Campos opcionais.
   - Defaults.
   - Validacao de path.
   - Validacao de escopo.

3. Padronizar saida JSON.
   - schema.
   - schema_version.
   - status.
   - intent.
   - risk_level.
   - planned_command.
   - executed.
   - return_code.
   - stdout_summary.
   - stderr_summary.
   - next_safe_step.

4. Criar testes negativos.
   - intent desconhecido.
   - cwd inexistente.
   - timeout invalido.
   - destructive sem dry_run.
   - push sem gate.
   - path fora do repo.
   - comando com token proibido.

### 9.3 Medio prazo - patches seguros

1. Criar patch runner.
   - Entrada: arquivo patch script em scripts/watcher.
   - Executa em modo dry-run quando possivel.
   - Sempre imprime status antes e depois.
   - Sempre roda diff check.
   - Nunca commita automaticamente sem flag.

2. Criar padrao de patch por fases.
   - inspect.
   - apply.
   - validate.
   - commit.
   - push.
   - final smoke.

3. Criar detector de modificacao parcial.
   - Se script falhar apos alterar arquivo, marcar estado como partial_change_detected.
   - Sugerir git diff e git restore seletivo.

4. Criar rollback helper.
   - Lista arquivos alterados.
   - Permite restaurar apenas arquivos de uma tentativa.
   - Nunca apaga arquivos untracked sem confirmacao.

### 9.4 Medio prazo - banco e dead letters

1. Melhorar relatorio de dead letters.
   - Agrupar por tipo.
   - Arupar por chat origem/destino.
   - Mostrar ultimos 20.
   - Mostrar recorrencias.
   - Sugerir correcao por padrao.

2. Criar limpeza segura.
   - Sempre dry-run primeiro.
   - Nunca deletar sem backup.
   - Backup antes de cleanup.
   - Log de limpeza em arquivo.

3. Criar compactacao de historico.
   - Backup DB.
   - Remover registros antigos por politica.
   - Validar integridade depois.

4. Criar painel textual de saude.
   - status_count.
   - invalid_messages.
   - dead_letters.
   - oldest_delivering.
   - db_size.
   - manifest_version.
   - head.
   - dirty state.

### 9.5 Medio prazo - extensao e UI

1. Melhorar deteccao de chat_id.
   - Confirmar chat atual.
   - Evitar source_chat_id_mismatch.
   - Mostrar aviso claro quando destino nao bate.

2. Melhorar entrega visual.
   - Detectar campo de texto correto.
   - Detectar botao correto.
   - Suportar mudancas de DOM.
   - Evitar duplicidade visual.

3. Melhorar dedupe.
   - Dedupe por command_id.
   - Dedupe por hash de envelope.
   - Dedupe por status entregue.

4. Melhorar feedback no chat.
   - Respostas curtas.
   - Erros com acao/correcao/modelo_seguro.
   - Linkar command_id original.

### 9.6 Medio prazo - documentacao

1. Manter este guia como documento ativo unico.
2. Atualizar este guia a cada tag relevante.
3. Arquivar documentos antigos em docs/archive.
4. Registrar:
   - versao.
   - commit.
   - tag.
   - o que mudou.
   - validacoes executadas.
   - riscos conhecidos.
   - proximas tarefas.
5. Criar uma secao de exemplos minimos por action.
6. Criar uma secao de anti-padroes.

### 9.7 Longo prazo - orquestracao entre chats

1. Criar protocolo de fiscalizacao.
   - Chat executor responde com plano.
   - Chat fiscal aprova ou corrige.
   - Executor roda read-only.
   - Fiscal verifica.
   - Executor aplica patch.
   - Fiscal valida evidencias.

2. Criar padrao de handoff.
   - Estado atual.
   - Arquivos alterados.
   - Validacoes.
   - Pendencias.
   - Proximo comando seguro.

3. Criar matriz de responsabilidade.
   - Chat supervisor.
   - Chat executor.
   - Chat fiscal.
   - Chat documentador.

4. Criar envelopes de ensino.
   - teach_watcher_basics.
   - teach_repo_safety.
   - teach_release_flow.
   - teach_failure_recovery.

### 9.8 Longo prazo - automacao operacional

1. Criar modo planejador.
   - Recebe objetivo.
   - Gera plano seguro.
   - Nao executa sem autorizacao.

2. Criar modo executor com gates.
   - Executa apenas intents aprovadas.
   - Exige validacoes entre fases.

3. Criar modo auditor.
   - Le git log.
   - Le tags.
   - Le docs.
   - Aponta divergencias.

4. Criar modo release manager.
   - Bump version.
   - Release check.
   - Commit.
   - Tag.
   - Push.
   - Status final.

---

## 10. Checklist operacional por tipo de tarefa

### 10.1 Estudar repo

- git status -sb.
- git log --oneline -5.
- listar docs.
- ler README ou guia.
- nao alterar arquivos.

### 10.2 Corrigir bug

- git status -sb.
- reproduzir ou localizar erro.
- aplicar patch pequeno.
- py_compile.
- smoke especifico.
- git diff --check.
- diff stat.
- reportar.

### 10.3 Atualizar documentacao

- git status -sb.
- inventariar docs.
- preservar historico.
- atualizar guia unico.
- git diff --check.
- docs smoke ou release_check.
- reportar arquivos alterados.

### 10.4 Fazer release

- repo limpo ou alteracoes esperadas.
- bump_version.
- py_compile.
- smokes.
- release_check.
- git diff --check.
- git add seletivo.
- commit.
- tag.
- push.
- push tag.
- git status -sb final.

### 10.5 Ensinar outro chat

- enviar mensagem curta.
- exigir ACK.
- exigir primeiro comando read-only.
- fiscalizar se nao pulou para escrita.
- corrigir qualquer action/delivery_kind/payload errado.

---

## 11. Anti-padroes proibidos

1. Reusar command_id.
2. Enviar envelope com markdown dentro dos marcadores.
3. Colocar message dentro de payload em send-chat-message.
4. Fazer script_text gigante com aspas aninhadas.
5. Aplicar Python indentado complexo dentro do JSON.
6. Fazer commit sem validar.
7. Fazer push sem release_check em mudanca operacional.
8. Usar cleanup sem dry-run.
9. Ignorar return_code 1 como se nada tivesse acontecido.
10. Insistir em patch sobre arquivo quebrado sem inspeccionar.
11. Apagar docs historicos sem arquivar.
12. Alterar varios subsistemas no mesmo commit sem necessidade.

---

## 12. Exemplos minimos

### 12.1 Status read-only

@@@AI_BRIDGE_LOCAL_START@@
{"command_id":"exemplo_status_read_only_001","source_chat_id":"chat","target_chat_id":"gateway-brain-supervisor","action":"run-command","delivery_kind":"local_capability","conversation_id":"exemplo","from_agent":"agente","payload":{"cwd":"D:/dev/autocode/ai-bridge-local","timeout_seconds":120,"command":["git","status","-sb"]}}
@@@AI_BRIDGE_LOCAL_END@@

### 12.2 Intent read-only

@@@AI_BRIDGE_LOCAL_START@@
{"command_id":"exemplo_intent_inspect_repo_001","source_chat_id":"chat","target_chat_id":"gateway-brain-supervisor","action":"run-command","delivery_kind":"local_capability","conversation_id":"exemplo","from_agent":"agente","payload":{"cwd":"D:/dev/autocode/ai-bridge-local","timeout_seconds":120,"intent":"inspect_repo"}}
@@@AI_BRIDGE_LOCAL_END@@

### 12.3 Mensagem para outro chat

@@@AI_BRIDGE_LOCAL_START@@{"command_id":"exemplo_send_chat_message_001","source_chat_id":"chat_origem","target_chat_id":"chat_destino","action":"send-chat-message","delivery_kind":"inter_agent_message","conversation_id":"exemplo","from_agent":"agente","message":"Mensagem curta para o chat destino.","payload":{}}
@@@AI_BRIDGE_LOCAL_END@@

---

## 13. Criterios de pronto

Uma atividade so deve ser considerada concluida quando houver:

1. Objetivo atendido.
2. Arquivos alterados listados.
3. Validacoes executadas.
4. Saida de erro analisada se existir.
5. git status final reportado.
6. Commit/tag/push apenas se solicitado ou se for release.
7. Documentacao atualizada quando houver mudanca operacional.

---

## 14. Proximas atividades recomendadas em ordem

1. Criar smoke para send-chat-message.
2. Criar intent inspect_delivery_failure.
3. Melhorar diagnostico de submit_button_not_found_or_disabled.
4. Criar intent validate_release.
5. Criar patch runner com dry-run.
6. Criar rollback helper.
7. Consolidar relatorio de dead letters por tipo.
8. Criar protocolo formal de fiscalizacao entre chats.
9. Melhorar docs smoke para garantir que este guia continue completo.
10. Criar release 0.4.45 somente depois de smokes e release_check OK.

---

## 15. Nota de manutencao

Este guia deve ser mantido como documento ativo principal. Quando uma nova versao for publicada, atualize:

- Versao atual.
- Tag mais recente.
- Commit de referencia.
- O que foi feito.
- Validacoes executadas.
- Proximas atividades.

Documentos antigos podem continuar no archive para historico, mas nao devem competir com este guia como fonte operacional ativa.

## 16. Marcadores historicos preservados para smoke_docs

Esta secao preserva explicitamente os marcadores que os smokes historicos ainda usam para garantir continuidade da documentacao consolidada.

- Diagnostics report: relatorio operacional de diagnostico do watcher, status, invalid messages e dead letters.
- Safe validation wrapper: camada de validacao segura antes de executar comandos locais sensiveis.
- Command builder smoke: smoke que garante que o command_builder gera envelopes validos.
- Diagnostics filters: filtros por target, command_prefix e limit para diagnostico operacional.
- Diagnostics viewer: visualizacao textual dos estados do banco local e eventos recentes.
- script_text/script_ext: mecanismo de script temporario usado apenas para scripts pequenos e controlados.
- Dead letters grouped report: relatorio agrupado de falhas persistentes por tipo, alvo e command_id.

Esses itens ja foram absorvidos no guia unificado, mas permanecem escritos literalmente aqui para compatibilidade com smoke_docs.py ate que o proprio smoke seja evoluido para validar a nova estrutura consolidada.

## Version alignment 0.4.45
The extension manifest name, extension manifest version, and VERSION file were aligned to 0.4.45. Future releases should use scripts/watcher/bump_version.py and scripts/watcher/smoke_version_alignment.py before tagging.

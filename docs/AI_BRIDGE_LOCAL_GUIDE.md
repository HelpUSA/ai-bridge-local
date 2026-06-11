# AI Bridge Local - Guia completo de aplicacao, operacao e comandos

Data-base: 2026-06-10
Projeto: `D/:dev/autocode/ai-bridge-local`
Versao operacional atual: `0.4.34`
Tag atual: `v0.4.34-virtual-workers-by-chat`

ATENCAO: este guia contem exemplos com marcadores reais do AI Bridge Local.
Se um exemplo for copiado e colado em um chat com a extensao ativa, ele pode ser interpretado como comando.
Use os exemplos somente quando quiser executar ou enviar o envelope.

## 1. Objetivo

Este guia consolida a documentacao operacional do AI Bridge Local em um unico arquivo.
Ele deve substituir os documentos incrementais antigos da pasta `docs/` depois de revisao.

O guia cobre a aplicacao, a arquitetura, os componentes, o protocolo de envelopes, exemplos reais de comandos, regras contra erros de JSON, uso de scripts, validacoes, smoke tests, troubleshooting e politica de limpeza dos docs.

## 2. Visao geral

O AI Bridge Local e uma ponte entre conversas do ChatGPT e o ambiente local da maquina.

Existem dois fluxos principais:

1. `send-chat-message`: envia mensagem de um chat para outro.
2. `run-command`: executa comando local por meio do gateway e do worker.

A extensao do navegador detecta envelopes no chat, envia ao gateway local, o gateway registra no banco SQLite, e o worker executa comandos locais quando necessario.

## 3. Componentes

### 3.1 Extensao do navegador

Arquivos:

- `extension/manifest.json`
- `extension/background.js`
- `extension/content_script.js`

Responsabilidades:

- detectar envelopes locais;
- enviar envelopes ao gateway;
- buscar mensagens pendentes;
- inserir mensagens no chat destino;
- confirmar entrega;
- reduzir duplicacao visual;
- apoiar cross-profile.

### 3.2 Gateway local

Arquivo:

- `gateway_local.py`

Porta usual:

- `127.0.0.1:8766`

Responsabilidades:

- receber envelopes;
- validar JSON;
- gravar mensagens e comandos em `queue_local.db`;
- expor mensagens pendentes para a extensao;
- expor comandos pendentes para o worker;
- registrar status como `queued`, `acked` e `failed`;
- devolver feedback quando o envelope e invalido.

### 3.3 Worker local

Arquivo:

- `brain_worker.py`

Responsabilidades:

- buscar comandos `run-command`;
- executar comandos no `cwd` informado;
- capturar `stdout`, `stderr` e `return_code`;
- devolver resultado ao `source_chat_id`;
- separar execucoes por origem no modelo de workers virtuais.

### 3.4 Banco local

Arquivo:

- `queue_local.db`

Uso:

- fila de mensagens inter-chat;
- fila de comandos locais;
- auditoria;
- diagnostico de mensagens presas ou duplicadas.

## 4. Arquitetura e fluxos

### 4.1 Fluxo `send-chat-message`

1. Chat origem emite envelope.
2. Extensao detecta o envelope.
3. Gateway grava mensagem para o `target_chat_id`.
4. Chat destino faz polling.
5. Extensao entrega mensagem no destino.
6. Gateway registra status.

Use para delegar tarefas, enviar status, treinar outro chat e coordenar frentes paralelas.

### 4.2 Fluxo `run-command`

Use para ler arquivos, validar codigo, aplicar patches, consultar Git e gerar relatorios locais.

1. Chat origem emite envelope `run-command`.
2. Gateway grava o comando local.
3. Worker busca comandos destinados a `gateway-brain-supervisor`.
4. Worker executa o comando.
5. Resultado volta ao `source_chat_id`.

### 4.3 Workers virtuais por chat

Na versao `0.4.34`, comandos locais sao separados por `source_chat_id`.
O destino local continua sendo `gateway-brain-supervisor`, mas a origem identifica quem pediu o comando e para onde o resultado deve voltar.

## 5. Protocolo de envelope

Todo envelope real usa marcadores locais sozinhos nas linhas de inicio e fim.

Modelo minimo:

```text
@@@AI_BRIDGE_LOCAL_START@@
{
  "schema": "ai_bridge_local.envelope",
  "schema_version": 1,
  "command_id": "exemplo_obrigatorio_001",
  "action": "send-chat-message",
  "source_chat_id": "SUBSTITUA_PELO_CHAT_ORIGEM",
  "target_chat_id": "SUBSTITUA_PELO_CHAT_DESTINO",
  "delivery_kind": "local_inter_agent_message",
  "conversation_id": "exemplo",
  "from_agent": "operador",
  "message": "Mensagem curta de exemplo."
}
@@AI_BRIDGE_LOCAL_ENDP@@
}```

Campos principais:

- `schema`: sempre `ai_bridge_local.envelope`.
- `schema_version`: atualmente `1`.
- `command_id`: unico por tentativa.
- `action`: `run-command` ou `send-chat-message`.
- `source_chat_id`: chat que emitiu.
- `target_chat_id`: destino.
- `delivery_kind`: tipo de entrega.
- `conversation_id`: agrupador logico.
- `from_agent`: identificacao do emissor.
- `payload`: usado em `run-command`.
- `message`: usado em `send-chat-message`.

Cada reenvio deve usar `command_id` novo.

## 6. Como usar `run-command`

Use `run-command` para executar comandos locais.

Regras obrigatorias:

- `target_chat_id`: `gateway-brain-supervisor`.
- `delivery_kind`: `local_capability`.
- `cwd`, `timeout_seconds` e `command` dentro de `payload`.
- Nao usar `target_chat_id: local`.
- Nao colocar `cwd` ou `command` no topo do JSON.

### 6.1 Exemplo real: git status

```text
@@AI_BRIDGE_LOCAL_START@@
{
  "schema": "ai_bridge_local.envelope",
  "schema_version": 1,
  "command_id": "example_git_status_001",
  "action": "run-command",
  "source_chat_id": "SUBSTITUA_PELO_CHAT_ORIGEM",
  "target_chat_id": "gateway-brain-supervisor",
  "delivery_kind": "local_capability",
  "conversation_id": "example_git_status",
  "from_agent": "operador",
  "payload": {
    "cwd": "D:/dev/autocode/ai-bridge-local",
    "timeout_seconds": 30,
    "command": [
      "cmd",
      "/c",
      "git status -sb"
    ]
  }
}
@@AI_BRIDGE_LOCAL_ENDP@@
}```

### 6.2 Exemplo real: listar docs

```text
@@@AI_BRIDGE_LOCAL_START@@
{
  "schema": "ai_bridge_local.envelope",
  "schema_version": 1,
  "command_id": "example_list_docs_001",
  "action": "run-command",
  "source_chat_id": "SUBSTITUA_PELO_CHAT_ORIGEM",
  "target_chat_id": "gateway-brain-supervisor",
  "delivery_kind": "local_capability",
  "conversation_id": "example_list_docs",
  "from_agent": "operador",
  "payload": {
    "cwd": "D:/dev/autocode/ai-bridge-local",
    "timeout_seconds": 30,
    "command": [
      "cmd",
      "/c",
      "git status -sb && dir docs"
    ]
  }
}
@@AI_BRIDGE_LOCAL_ENDP@@
}```

### 6.3 Exemplo real: validacoes principais

```text
@@AI_BRIDGE_LOCAL_START@@
{
  "schema": "ai_bridge_local.envelope",
  "schema_version": 1,
  "command_id": "example_validate_project_001",
  "action": "run-command",
  "source_chat_id": "SUBSTITUA_PELO_CHAT_ORIGEM",
  "target_chat_id": "gateway-brain-supervisor",
  "delivery_kind": "local_capability",
  "conversation_id": "example_validate_project",
  "from_agent": "operador",
  "payload": {
    "cwd": "D:/dev/autocode/ai-bridge-local",
    "timeout_seconds": 120,
    "command": [
      "cmd",
      "/c",
      "node --check extension/background.js && node --check extension/content_script.js && python -m py_compile gateway_local.py brain_worker.py && git diff --check && git status -sb"
    ]
  }
}
@@@AI_BRIDGE_LOCAL_ENDP@@
}```

## 7. Como usar `send-chat-message`

Use `send-chat-message` para enviar texto a outro chat.

Regras:

- `target_chat_id`: chat destino real.
- `delivery_kind`: `local_inter_agent_message`.
- Campo `message`: texto curto.
- Evitar JSON grande dentro de `message`.
- Evitar mensagem enorme em uma unica tentativa.

### 7.1 Exemplo real: mensagem simples

```text
@@AI_BRIDGE_LOCAL_START@@
{
  "schema": "ai_bridge_local.envelope",
  "schema_version": 1,
  "command_id": "example_send_message_001",
  "action": "send-chat-message",
  "source_chat_id": "SUBSTITUA_PELO_CHAT_ORIGEM",
  "target_chat_id": "SUBSTITUA_PELO_CHAT_DESTINO",
  "delivery_kind": "local_inter_agent_message",
  "conversation_id": "example_inter_chat",
  "from_agent": "operador",
  "message": "Mensagem de teste enviada pelo AI Bridge Local."
}
@@AI_BRIDGE_LOCAL_ENDP@@
}```

### 7.2 Exemplo real: delegar leitura read-only

```text
@@AI_BRIDGE_LOCAL_START@@
{
  "schema": "ai_bridge_local.envelope",
  "schema_version": 1,
  "command_id": "example_delegate_readonly_docs_001",
  "action": "send-chat-message",
  "source_chat_id": "SUBSTITUA_PELO_CHAT_ORIGEM",
  "target_chat_id": "SUBSTITUA_PELO_CHAT_DESTINO",
  "delivery_kind": "local_inter_agent_message",
  "conversation_id": "example_docs_review",
  "from_agent": "operador",
  "message": "Leia a pasta docs em modo read-only. Nao altere arquivos. Responda com lista, resumo e proximo passo."
}
@@AI_BRIDGE_LOCAL_ENDP@@
}```

## 8. Erros comuns e regras anti JSON quebrado

### 8.1 `envelope_parse_error`

Causas comuns:

- aspas curvas;
- caracteres invisiveis;
- string com quebra de linha invalida;
- barra invertida em caminho Windows;
- comando inline grande;
- PowerShell complexo;
- JSON dentro de `message`;
- marcadores antigos;
- `target_chat_id: local`;
- `cwd` e `command` fora de `payload`.

Correcao:

1. Criar `command_id` novo.
2. Reduzir o envelope.
3. Usar aspas duplas ASCII.
4. Preferir barras normais `/`.
5. Evitar PowerShell grande inline.
6. Usar `script_text`, `script_ext` ou arquivo real.

### 8.2 Formato antigo incorreto

Errado:

```json
{{
  "action": "run-command",
  "target_chat_id": "local",
  "cwd": "D:/dev/autocode/ai-bridge-local",
  "command": ["cmd", "/c", "git status -sb"]
}}
```

Correto:

```json
{{
  "action": "run-command",
  "target_chat_id": "gateway-brain-supervisor",
  "delivery_kind": "local_capability",
  "payload": {{
    "cwd": "D:/dev/autocode/ai-bridge-local",
    "timeout_seconds": 30,
    "command": ["cmd", "/c", "git status -sb"]
  }}
}}
```

### 8.3 Caminhos Windows

Evitar:

```text
D:\dev\autocode\ai-bridge-local
```

Preferir:

```text
D:/dev/autocode/ai-bridge-local
```

## 9. Scripts grandes

Para tarefas grandes, evitar `python -c` ou PowerShell inline muito longo.

Preferir:

- `payload.script_text` com `payload.script_ext`, quando suportado;
- script real em `temp/`;
- script real em `scripts/watcher/`;
- comando curto chamando o arquivo.

Politica:

- script temporario deve ser removido se nao for permanente;
- nao commitar script temporario sem autorizacao;
- reportar quais scripts foram criados;
- validar depois de qualquer patch.

## 10. Validacoes obrigatorias

Antes de commit, rodar:

```text
node --check extension/background.js
node --check extension/content_script.js
python -m py_compile gateway_local.py brain_worker.py
git diff --check
git status -sb
git diff --stat
```

## 11. Smoke tests

### 11.1 Smoke de `run-command`

Enviar comando simples:

```text
echo SMOKE_OK && git status -sb
```

Esperado:

- `status=acked`;
- `return_code=0`;
- `stdout` contem `SMOKE_OK`.

### 11.2 Smoke de `send-chat-message`

Enviar mensagem curta para outro chat.

Esperado:

- resultado `acked`;
- metodo coerente, como `button_click_confirmed`;
- mensagem aparece no destino.

### 11.3 Smoke de worker virtual

Enviar comandos de duas origens diferentes e confirmar que cada resultado volta ao seu `source_chat_id`.

## 12. Tags e versoes importantes

- `v0.4.13-local-run-command-0.2.1`: base de run-command local.
- `v0.4.14-confirm-send-before-ack`: confirmacao de envio antes de ACK.
- `v0.4.16-submit-recovery`: recuperacao de submit.
- `v0.4.17-visual-dedupe-temp-script`: dedupe visual.
- `v0.4.34-virtual-workers-by-chat`: workers virtuais por chat.

## 13. Troubleshooting

### Mensagem ficou `queued`

Verificar:

1. chat destino aberto;
2. extensao ativa;
3. F5 no destino;
4. `target_chat_id` correto;
5. gateway rodando;
6. banco local.

### ACK sem mensagem visivel

Verificar:

1. metodo de entrega;
2. chat correto;
3. falha de submit;
4. duplicacao visual;
5. status no banco.

### `stdout` truncado

Solucoes:

1. ler em partes;
2. filtrar saida;
3. gravar saida em arquivo temporario;
4. resumir antes de retornar.

## 14. Politica de limpeza dos docs

A pasta `docs/` acumulou documentos incrementais. O processo correto e:

1. Criar e revisar `docs/AI_BRIDGE_LOCAL_GUIDE.md`.
2. Confirmar que cobre aplicacao, comandos, validacoes e troubleshooting.
3. Rodar `git diff --check`.
4. Fazer dry-run listando documentos antigos.
5. Aguardar autorizacao de Wagner.
6. Mover para `docs/archive/` ou remover em commit separado.

Nunca apagar documentos antigos antes de revisar este guia consolidado.

## 15. Checklist rapido

### Para `run-command`

- `action`: `run-command`
- `target_chat_id`: `gateway-brain-supervisor`
- `delivery_kind`: `local_capability`
- `payload.cwd`
- `payload.timeout_seconds`
- `payload.command`

### Para `send-chat-message`

- `action`: `send-chat-message`
- `target_chat_id`: chat destino
- `delivery_kind`: `local_inter_agent_message`
- `message`: texto curto

### Para evitar erro

- JSON estrito;
- aspas duplas ASCII;
- `command_id` novo;
- barras normais;
- sem PowerShell grande inline;
- sem `target_chat_id: local`;
- sem `cwd` e `command` no topo;
- usar script real para tarefas grandes.

## 16. Conclusao

O AI Bridge Local deve ser operado com envelopes validos, comandos pequenos e validacoes frequentes.

A separacao principal e:

- `send-chat-message` para conversar com outro chat;
- `run-command` para executar localmente via `gateway-brain-supervisor`.

A versao `0.4.34` consolida o modelo de workers virtuais por `source_chat_id`, permitindo operacao livre por varios chats sem misturar resultados.


## Roadmap v0.5.0 - AI Bridge Local Control Center
### Atividade futura - telemetria do service worker e eventos da extensao

Hoje o watcher le com boa confiabilidade o que chega ao gateway, ao banco e a fila local, mas isso nao garante visibilidade completa de tudo que passa internamente pelo service worker da extensao (`background.js`) ou pelo `content_script.js`. Para o Control Center da versao v0.5.0, deve ser implementada uma trilha de diagnostico enviada pela extensao ao gateway e persistida na tabela `events`.

Eventos recomendados: `envelope_detected`, `envelope_parse_error`, `envelope_semantic_error`, `postCommand_attempt`, `postCommand_ok`, `postCommand_failed`, `delivery_attempt`, `delivery_ok`, `delivery_failed`, `chat_heartbeat`, `extension_version` e `active_chat_seen`.

Essa telemetria deve alimentar o Control Center para permitir ver mensagens recebidas, erros, status por chat, versao da extensao ativa, falhas de entrega, heartbeat por chat e um diagnostico copiavel para suporte. O objetivo e reduzir casos silenciosos e separar claramente erro de parse, erro semantico, falha de envio ao gateway e falha de entrega ao chat destino.

Regra obrigatoria: um `send-chat-message` semanticamente invalido, por exemplo com `payload.message` preenchido mas sem `message` top-level, deve gerar `AI_LOCAL_SEMANTIC_ERROR` ou `AI_LOCAL_ERROR` no chat de origem e nao pode ser enfileirado, executado ou ignorado silenciosamente.


Esta e a proxima frente do projeto. O objetivo e transformar o AI Bridge Local em um aplicativo Windows instalavel, com janela grafica elegante, botoes de controle, tray icon, atualizacao segura e visao operacional dos chats ativos.

### Nome sugerido

```text
AI Bridge Local Control Center
```

### Objetivo

Criar um executavel Windows que seja o ponto unico de controle do ambiente local. Ele deve substituir o uso diario de varios arquivos `.bat` ou terminais separados.

O usuario deve poder iniciar, parar, reiniciar, atualizar e acompanhar o gateway, o worker e as filas por chat de forma visual.

### Comportamento do applicativo

O applicativo deve ter uma janela padrao Windows. Ao clicar no botao de fechar, o app nao deve encerrar os servicos imediatamente. Ele deve ficar minimizado na bandeja do Windows, perto do relogio.

O icone da bandeja deve ter opcoes para:

```text
Abrir painel
Iniciar tudo
Parar tudo
Reiniciar tudo
Atualizar
Abrir logs
Sair de verdade
```

### Painel principal

A tela inicial deve mostrar, no minimo:

```text
Gateway/Supervisor: ligado ou desligado
Worker/Worker pool: ligado ou desligado
Banco/fila local: OK ou erro
Ultima atividade
Ultimo comando
Ultimo ACK
Ultimo erro
Versao local do AI Bridge
Commit atual
Tag atual
```

Botoes princiqpais:

```text
Iniciar tudo
Parar tudo
Reiniciar tudo
Atualizar
Abrir documentacao
Abrir pasta do projeto
Copiar diagnostico
```

### Console ao vivo do worker

O Control Center deve ter uma area de console ao vivo para mostrar o que hoje aparece na janela do `worker.bat` ou `worker_pool.bat`.

Essa area e importante porque serve para acompanhamento e para permitir copiar logs e falhas para colar no chat durante a depuracao.

Funcoes desejadas:

```text
Copiar log
Salvar log
Limpar tela
Pausar rolagem
Filtrar por chat
Filtrar por error
Filtrar por command_id
```

### Chats ativos e filas por chat

O applicativo deve mostrar uma tabela com cada chat ativo detectado. Isso deve usar a aquitetura ja implementada de workers virtuais por `source_chat_id`.

Campos desejados:

```text
Nome ou apelido do chat
chat_id
source_chat_id
status
ultima atividade
fila pendente
comando em execucao
ultimo ACK
ultimo error
conversation_id atual
adapter
versao da extensao
versao do protocolo local
```

### Heartbeat da extensao

Para mostrar chats ativos com versao da extensao, a extensao do navegador deve enviar um heartbeat periodico para o gateway local.

Payload sugerido:

```json
{
  "chat_id": "...",
  "source_chat_id": "...",
  "extension_version": "0.4.34",
  "protocol_version": "0.4.34",
  "adapter": "browser_extension_direct",
  "last_seen": "...",
  "page_title": "...",
  "url_host": "chatgpt.com",
  "conversation_id": "..."
}
```

### Atualizacao

O applicativo deve ter uma area de atualizacao, pois o projeto deve ser atualizado com frequencia.

Fluxo seguro desejado:

```text
Werificar atualizacao
Mostrar versao atual
Mostrar commit atual
Parar gateway e worker
Fazer backup de queue_local.db e configs
Aplicar atualizacao
Atualizar dependencias, se necessario
Validar aquivos principais
Reiniciar servicos
Mostrar resultado
Permitir rollback basico se falhar
```

Tipos de atualizacao:

```text
Atualizar app desktop
Atualizar gateway/worker
Atualizar extensao
Atualizar documentacao
Atualizar tudo
```

### Diagnostico copiavel

O applicativo deve ter botao para gerar um diagnostico copiavel, contendo:

```text
versao do app
versao da extensao
commit atual
tag atual
status do gateway
status do worker
chats ativos
filas pendentes
ultimos erros
ultimos command_id executados
porta local
caminho do projeto
```

### Tecnologia recomendada

Primeira versao:

```text
Python + PySide6
PyInstaller
Inno Setup em fase posterior
```

### Fases de implementacao

```text
Fase 1: painel basico com iniciar, parar, reiniciar, console ao vivo e tray icon
Fase 2: tabela de chats ativos, filas por source_chat_id e estatus
Fase 3: atualizacao com backup, validacao, reinicio e rollback
```

### Estado atual

Esta frente ainda nao foi implementada. Ela esta registrada como especificacao inicial para iniciar a versao `v0.5.0`.


### Telemetria futura do service worker e eventos da extensão

Hoje o watcher consegue inspecionar principalmente o que chega ao gateway local, ao banco `queue_local.db`, às filas e aos registros de execução. Nem toda mensagem que passa internamente pelo `content_script.js` ou pelo `background.js`/service worker fica visível depois, porque o service worker pode processar algo sem persistir evento, log ou feedback.

Atividade futura: adicionar telemetria explícita da extensão para o gateway local e para a tabela `events`. O objetivo é permitir que o watcher e o futuro Control Center mostrem o histórico operacional da extensão, inclusive mensagens detectadas, erros de parse, erros semânticos, tentativas de envio, falhas de entrega, chats ativos e versões da extensão.

Eventos desejados:

```text
envelope_detected
envelope_parse_error
envelope_semantic_error
postCommand_attempt
postCommand_ok
postCommand_failed
delivery_attempt
delivery_ok
delivery_failed
chat_heartbeat
extension_version
active_chat_seen
```

Esses eventos devem alimentar o Control Center para exibir status por chat, `source_chat_id`, última atividade, versão da extensão, falhas recentes, comandos recebidos, comandos entregues e diagnóstico copiável.

Regra específica: um `send-chat-message` semanticamente inválido, por exemplo com `payload.message` preenchido mas sem `message` top-level string não vazia, não pode ser aceito silenciosamente. A extensão e o gateway devem gerar `AI_LOCAL_SEMANTIC_ERROR` ou `AI_LOCAL_ERRO` no chat de origem, com orientação `corrija_e_reenvie`, preservando o `command_id` original quando possível e garantindo que nada seja enfileirado como mensagem vazia.

### Implementado em 2026-06-10 - Central de Controle JSON

Primeira etapa da Central de Controle implementada no gateway local.
Entradas disponiveis apos reiniciar o gateway:
- /control
- /control/status

Ambas retornam JSON com ok, service, version, timestamp, contagem por status de comandos, comandos recentes e eventos recentes.
Validado com python -m py_compile, git diff --check e smoke via curl apos restart do gateway.

### Central de Controle Windows residente

A Central de Controle evoluira para aplicativo Windows instalado, com janela propria, icone residente na bandeja do sistema e continuidade operacional ao fechar a janela. A especificacao inicial esta em docs/WINDOWS_CONTROL_CENTER_APP.md.

## Atualizacao operacional 2026-06-11

Esta secao consolida o estado validado apos os testes bidirecionais e substitui documentos incrementais antigos como fonte operacional diaria.

### Estado atual validado

- Extensao AI Bridge Local 0.4.35 operacional.
- Gateway local em 127.0.0.1:8766 com SQLite queue_local.db.
- Worker local usa target_chat_id gateway-brain-supervisor para run-command.
- Control Center Windows existente em app_windows/control_center_app.py.
- Comunicacao bidirecional validada por ACK entre este chat e o chat 6a298922-7530-83e9-8561-6474480a6a53.
- Repo D:/dev/autocode/ai-bridge-local limpo e alinhado em main...origin/main durante a validacao.

### Commits recentes relevantes

- 0e747c4 Fix gateway stale delivery watchdog 0.2.3.
- 307705f Add gateway stale delivery watchdog 0.2.2.
- e89c1ab Add outer inject timeout and bump extension 0.4.35.
- d844139 Harden extension tab message timeout.
- df860d3 Align extension runtime version 0.4.34.
- 14843fe Add extension inject timeout and bump version.
- ee99cf3 Improve local control center latency.

### Regras operacionais consolidadas

- send-chat-message deve usar message top-level; nao usar payload.message para mensagem inter-chat.
- delivery_kind para comunicacao inter-chat deve ser local_inter_agent_message.
- run-command deve usar target_chat_id gateway-brain-supervisor, delivery_kind local_capability e payload.cwd, payload.timeout_seconds, payload.command.
- Cada tentativa deve usar command_id novo.
- Evitar placeholders como {json} ou { JSON estrito } em mensagens com marcadores reais.
- Evitar markdown, crases e exemplos ilustrativos quando o objetivo for executar envelope real.
- Evitar script_text grande, aspas aninhadas, quebras invalidas, barras invertidas Windows em JSON e caracteres invisiveis.
- Para tarefas grandes, criar script real pequeno em scripts/watcher ou temp e executar comando curto.

### Problemas recentes e resolucoes

- Falhas recentes foram causadas por JSON fragil, payload.message incorreto, placeholders e composer ocupado no chat destino.
- Essas falhas nao indicaram problema estrutural do bridge.
- O watchdog do gateway agora marca send-message e send-chat-message presos em delivering por mais de 45 segundos como failed com last_error stale delivering timeout after extension delivery.
- A extensao 0.4.35 adiciona callback timeout e outer inject timeout no background.

### Proximas atividades prioritarias

1. Fechar smoke oficial 0.4.35 em dois ou tres chats com send-chat-message e run-command.
2. Corrigir a versao HTTP do gateway caso /health ainda mostre 0.2.1 apesar do watchdog 0.2.3 funcional.
3. Implementar telemetria da extensao para a tabela events: envelope_detected, envelope_parse_error, envelope_semantic_error, postCommand_attempt, postCommand_ok, postCommand_failed, delivery_attempt, delivery_ok, delivery_failed, chat_heartbeat, extension_version e active_chat_seen.
4. Melhorar diagnostico do chat destino para casos como destino nao registrado, tabId antigo, composer nao encontrado, botao desabilitado, inject timeout e runtime error.
5. Preparar v0.5.0 do Control Center com tabela de chats ativos, heartbeat por chat, ultimos ACKs e erros, botao copiar diagnostico, console ao vivo e atualizacao segura.

### Documento antigo arquivado

- O status incremental docs/legacy/AI_BRIDGE_LOCAL_CURRENT_STATUS_2026-06-10.md foi arquivado em docs/archive porque este guia passou a ser a referencia principal consolidada.

## Complemento operacional 2026-06-11 - smoke 0.4.35 e diagnostico

- Gateway HTTP atualizado para 0.2.3 para refletir o watchdog stale delivery funcional.
- Smoke oficial 0.4.35 deve cobrir run-command via gateway-brain-supervisor e send-chat-message com message top-level.
- Falhas inter-chat devem registrar diagnostico objetivo: composer ocupado, botao desabilitado, timeout de inject, destino nao registrado, tabId antigo ou stale delivering timeout.
- Telemetria futura da extensao deve persistir envelope_detected, envelope_parse_error, envelope_semantic_error, postCommand_attempt, postCommand_ok, postCommand_failed, delivery_attempt, delivery_ok, delivery_failed, chat_heartbeat, extension_version e active_chat_seen.
- Control Center v0.5.0 deve exibir chats ativos, heartbeat, ultimos ACKs, ultimos erros, console ao vivo, copiar diagnostico e atualizacao segura.

## Status operacional consolidado - 2026-06-11

- AI Bridge Local 0.4.35 operacional; comunicacao bidirecional validada; send-chat-message com message top-level; run-command via gateway-brain-supervisor.
- Gateway 127.0.0.1:8766 com HTTP/runtime 0.2.3; watchdog stale delivery ativo; queue_local.db sem delivering preso apos watchdog.
- Smoke run-command OK; smoke send-chat-message OK com button_click_confirmed; Control Center Windows existente.
- Commits relevantes: b26f1cd docs principal/archive; ab4bc59 gateway version/docs; 0e747c4 watchdog 0.2.3; e89c1ab extensao 0.4.35; ee99cf3 latencia Control Center.

### Regras operacionais atuais
- JSON estrito; command_id novo; sem placeholders; sem markdown/crases ao executar envelope real; evitar script_text grande e aspas aninhadas; usar script real para tarefas grandes.
- send-chat-message usa message top-level e delivery_kind local_inter_agent_message; run-command usa payload.cwd, payload.timeout_seconds e payload.command.

### Proximas atividades
1. Criar tag v0.4.35-stable-docs-gateway-0.2.3.
2. Implementar telemetria minima da extensao em events: chat_heartbeat, extension_version, delivery_attempt, delivery_ok, delivery_failed, envelope_parse_error, envelope_semantic_error.
3. Rodar smoke multi-chat pos-tag em 2 ou 3 chats.
4. Iniciar Control Center v0.5.0 fase 1 com tabela de chats ativos, ultima atividade, versao da extensao, ultimos ACK/falhas, copiar diagnostico e console ao vivo.
5. Melhorar diagnostico de falha visual no destino: destino nao registrado, tabId antigo, composer nao encontrado, botao desabilitado, runtime error e inject timeout.
6. Preparar atualizacao segura no Control Center: parar servicos, backup queue_local.db, git pull, validacoes, reinicio e rollback basico.

## Conteudo consolidado dos documentos movidos para legacy

### Documento legado consolidado: WINDOWS_CONTROL_CENTER_APP.md
# AI Bridge Local - Aplicativo Windows residente

Data-base: 2026-06-10

## Decisao de produto

A Central de Controle nao sera apenas uma tela HTML. Ela sera um aplicativo Windows instalado na maquina, com janela propria, icone residente na bandeja do sistema e comportamento de continuar ativo quando a janela for fechada.

## Caracteristicas esperadas

- Instalar no Windows como aplicacao local.
- Subir e supervisionar gateway_local.py e brain_worker.py.
- Mostrar status do gateway, fila, comandos recentes e eventos recentes.
- Usar os endpoints locais /control e /control/status como API de leitura.
- Ao fechar a janela, minimizar para a bandeja do sistema.
- Ter menu no icone da bandeja com abrir, reiniciar servicos e sair.
- Incluir empacotamento para gerar executavel e instalador.
- Manter compatibilidade com a extensao do navegador e com o banco queue_local.db.

## Dependencias previstas

A base Python atual possui tkinter e PIL. Para a versao residente completa serao adicionadas dependencias de empacotamento e bandeja: pystray, psutil e PyInstaller.

## Estrutura proposta

- app_windows/control_center_app.py: aplicacao desktop residente.
- app_windows/requirements-windows-app.txt: dependencias do app.
- packaging/build_windows_app.ps1: build do executavel.
- packaging/install_windows_app.ps1: instalacao local inicial.

## Fase 1

Criar scaffold executavel com tkinter, leitura de /control/status, botao de atualizar, botoes de restart do gateway e worker, e comportamento de minimizar para bandeja quando pystray estiver instalado.

## Fase 2

Gerar executavel com PyInstaller e preparar instalador Windows com atalho e inicializacao automatica opcional.

## Fase 3

Adicionar UI completa, logs, status por chat, diagnostico copiavel e configuracao visual.

## Atualizacao 2026-06-11 - requisitos v0.5.0

- Tabela de chats ativos com chat_id, source_chat_id, ultima atividade, fila pendente e comando em execucao.
- Heartbeat por chat enviado pela extensao ao gateway.
- Ultimos ACKs e erros por chat, console ao vivo, filtros, copiar diagnostico e atualizacao segura.
- Diagnostico claro para destino nao registrado, tabId antigo, composer nao encontrado, botao desabilitado, inject timeout e runtime error.


### Documento legado consolidado: archive/AI_BRIDGE_LOCAL_CURRENT_STATUS_2026-06-10.md
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


## Status operacional 2026-06-11

- AI Bridge Local 0.4.35 operacional.
- Comunicacao bidirecional validada.
- send-chat-message validado com message top-level e delivery_kind local_inter_agent_message.
- run-command somente via gateway-brain-supervisor com delivery_kind local_capability e payload.cwd, payload.timeout_seconds e payload.command.
- Gateway em 127.0.0.1:8766.
- Gateway HTTP/runtime alinhado para 0.2.3.
- Watchdog stale delivery ativo para evitar delivering infinito.
- queue_local.db sem delivering preso apos watchdog.
- Control Center Windows existente.
- Repo limpo e alinhado com origin/main no fechamento validado.
- Smoke run-command OK.
- Smoke send-chat-message OK.
- Aviso CRLF no Windows pode aparecer sem indicar falha.

### Commits relevantes

- b26f1cd consolidou docs/AI_BRIDGE_LOCAL_GUIDE.md como documento principal e moveu docs/legacy/AI_BRIDGE_LOCAL_CURRENT_STATUS_2026-06-10.md para docs/archive/AI_BRIDGE_LOCAL_CURRENT_STATUS_2026-06-10.md.
- ab4bc59 atualizou versao HTTP/runtime do gateway e docs.
- 0e747c4 corrigiu watchdog stale delivery 0.2.3.
- e89c1ab adicionou outer inject timeout e extensao 0.4.35.
- f947c25 consolidou a documentacao do AI Bridge Local no guia principal.

### Regras de operacao atuais

- Usar JSON estrito.
- Usar command_id novo a cada tentativa.
- send-chat-message deve usar message top-level e delivery_kind local_inter_agent_message.
- run-command deve usar target_chat_id gateway-brain-supervisor, delivery_kind local_capability e payload.cwd, payload.timeout_seconds e payload.command.
- Nao usar placeholders como {json} ou exemplos incompletos em envelope real.
- Nao usar markdown ou crases quando o objetivo for executar envelope real.
- Evitar script_text grande, aspas aninhadas, quebras invalidas e caracteres invisiveis.
- Para tarefas grandes, usar script real em scripts/watcher ou temp e executar comando curto.

### Proximas atividades

1. Criar ou confirmar tag v0.4.35-stable-docs-gateway-0.2.3.
2. Implementar telemetria minima da extensao em events com chat_heartbeat, extension_version, delivery_attempt, delivery_ok, delivery_failed, envelope_parse_error e envelope_semantic_error.
3. Rodar smoke multi-chat pos-tag em dois ou tres chats.
4. Iniciar Control Center v0.5.0 fase 1 com tabela de chats ativos, ultima atividade, versao da extensao, ultimos ACK/falhas, copiar diagnostico e console ao vivo.
5. Melhorar diagnostico de falha visual no destino: destino nao registrado, tabId antigo, composer nao encontrado, botao desabilitado, runtime error e inject timeout.
6. Preparar atualizacao segura no Control Center com parar servicos, backup queue_local.db, git pull, validacoes, reinicio e rollback basico.


## Proxima evolucao: Command Gateway, Builder, Validator e quarentena

Objetivo: reduzir dependencia de envelopes JSON crus gerados diretamente por chats. O chat deve declarar uma intencao curta; uma camada local deve montar o envelope completo, validar por contrato formal e permitir que apenas comandos validos entrem na fila principal.

Diagnostico operacional: comandos longos com JSON inline, scripts grandes, escapes, aspas ou caracteres invisiveis podem quebrar antes de chegar ao executor. O resultado e tentativa perdida, retrabalho manual e risco de travar o fluxo. A solucao e adicionar uma borda de validacao e roteamento.

Padroes adotados como referencia:
- Contrato formal com JSON Schema para campos obrigatorios, tipos, enums, limites e formatos.
- Validacao na borda antes de inserir em queue_local.db.
- Invalid Message Channel para JSON ruim, schema errado, placeholders, caracteres invisiveis, aspas curvas e erros semanticos.
- Dead Letter Queue para comandos validos que falham apos tentativas, entrega ou execucao.
- Retry limitado com backoff e idempotencia.
- Structured outputs para origem LLM, sempre com validacao local.
- Comandos grandes por referencia a scripts reais em scripts/watcher, nao por payload inline grande.

Fluxo recomendado:
1. Chat escreve uma intencao curta.
2. Envelope Builder local transforma a intencao em JSON completo e seguro.
3. Validator aplica contrato formal e regras semanticas.
4. Gateway grava em commands apenas se o comando for valido.
5. Extension entrega e registra telemetria.
6. Invalidos antes da fila vao para invalid_messages.
7. Validos aceitos que falham de forma persistente vao para dead_letters.

Exemplos de intencao segura:
text
AI_LOCAL_INTENT send_chat target=6a2b0a05 message=ACK recebido
AI_LOCAL_INTENT run cwd=D:/dev/autocode/ai-bridge-local command=git status -sb
AI_LOCAL_INTENT run_script cwd=D:/dev/autocode/ai-bridge-local script=scripts/watcher/check_status.py


Artefatos planejados:
- schemas/ai_bridge_local_envelope.schema.json como contrato oficial inicial.
- command_builder.py para gerar envelopes seguros.
- Preflight validator no gateway antes do insert em commands.
- Tabela invalid_messages para rejeicoes antes da fila.
- Tabela dead_letters para falhas persistentes depois de aceitas.
- Painel no Control Center para validar envelope, copiar comando seguro, ver invalidos, ver DLQ e reprocessar apos correcao.

Ordem de implementacao:
1. Criar JSON Schema oficial dos envelopes.
2. Adicionar preflight validator no gateway.
3. Criar invalid_messages.
4. Criar command_builder.py.
5. Bloquear placeholders, aspas curvas, caracteres invisiveis e payload grande.
6. Migrar comandos grandes para scripts reais.
7. Expor invalidos e dead letters no Control Center.

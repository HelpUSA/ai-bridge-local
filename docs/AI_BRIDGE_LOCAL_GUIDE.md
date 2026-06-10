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

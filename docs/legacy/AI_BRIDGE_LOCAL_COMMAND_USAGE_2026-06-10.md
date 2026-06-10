# AI Bridge Local - exemplos de comandos e cuidados 2026-06-10

## Regra principal

Para textos, scripts ou consultas grandes, nao embutir tudo dentro de JSON no chat.

Use esta ordem:

1. Comando curto em payload.command.
2. Script temporario real em temp/ ou scripts/.
3. Executar o arquivo com python arquivo.py ou powershell -File arquivo.ps1.
4. No futuro, implementar SCRIPT_COMMAND com corpo bruto fora do JSON.

## Formato local obrigatorio

Os marcadores locais devem ficar sozinhos nas linhas de inicio e fim:

@@AI_BRIDGE_LOCAL_START@@
{ JSON valido }
@@AI_BRIDGE_LOCAL_END@@

Nao usar BRIDGE_ASSISTANT_COMMAND nesta aplicacao local.

## Exemplo: enviar mensagem para outro chat

Campos essenciais:

- command_id: identificador unico.
- action: send-chat-message.
- source_chat_id: chat origem.
- target_chat_id: chat destino.
- delivery_kind: local_inter_agent_message.
- message: texto a ser enviado ao destino.

Modelo:

{
  "schema": "ai_bridge_local.envelope",
  "schema_version": 1,
  "command_id": "exemplo_envio_001",
  "action": "send-chat-message",
  "source_chat_id": "chat-origem",
  "target_chat_id": "chat-destino",
  "delivery_kind": "local_inter_agent_message",
  "conversation_id": "exemplo",
  "from_agent": "agente origem",
  "message": "Mensagem de teste."
}

## Exemplo: executar comando local

Campos essenciais:

- action: run-command.
- target_chat_id: gateway-brain-supervisor.
- delivery_kind: local_capability.
- payload.cwd: pasta de trabalho.
- payload.timeout_seconds: limite de tempo.
- payload.command: array de argumentos ou string simples.

Modelo:

{
  "schema": "ai_bridge_local.envelope",
  "schema_version": 1,
  "command_id": "run_exemplo_001",
  "action": "run-command",
  "source_chat_id": "chat-origem",
  "target_chat_id": "gateway-brain-supervisor",
  "delivery_kind": "local_capability",
  "conversation_id": "run_exemplo",
  "from_agent": "agente origem",
  "payload": {
    "cwd": "D:/dev/autocode/ai-bridge-local",
    "timeout_seconds": 30,
    "command": [
      "cmd",
      "/c",
      "echo OK && cd"
    ]
  }
}

## Exemplo: PowerShell curto

{
  "payload": {
    "cwd": "D:/dev/autocode/ai-bridge-local",
    "timeout_seconds": 60,
    "command": [
      "powershell",
      "-NoProfile",
      "-ExecutionPolicy",
      "Bypass",
      "-Command",
      "git status -sb; git diff --check"
    ]
  }
}

## Exemplo: script grande

Para script grande, criar arquivo real primeiro.

Exemplo seguro:

1. Criar um arquivo em temp/meu_script.py.
2. Colocar o codigo dentro dele.
3. Executar com python ./temp/meu_script.py.
4. Se for via bridge, chamar apenas o arquivo pelo payload.command.

Payload para executar arquivo ja criado:

{
  "payload": {
    "cwd": "D:/dev/autocode/ai-bridge-local",
    "timeout_seconds": 60,
    "command": [
      "python",
      "./temp/meu_script.py"
    ]
  }
}

## O que evitar

- Nao embutir Python, PowerShell, SQL ou Markdown grande diretamente em payload.command.
- Nao usar barras invertidas sem escape dentro de JSON.
- Preferir caminhos com barras normais: ./extension/background.js e D:/dev/autocode/ai-bridge-local.
- Nao usar python - <<PY no PowerShell.
- Nao usar python -c grande.
- Nao confiar apenas em clique de botao para ACK.
- Nao commitar scripts temporarios one-off.

## Como diagnosticar cross-profile

1. Confirmar que o outro perfil tem a extensao carregada.
2. Recarregar extensao em chrome://extensions.
3. Dar F5 no chat destino.
4. Verificar queue_local.db.
5. Se status for queued, o destino nao esta pollando.
6. Se status for acked, mas nada apareceu, investigar injecao no composer.
7. Se aparece duplicado visualmente, consultar duplicatas reais no banco antes de patchar.

## Validacao antes de commit

Rodar sempre:

node --check ./extension/background.js
node --check ./extension/content_script.js
python -m py_compile ./gateway_local.py ./brain_worker.py
git diff --check
git status -sb
git diff --stat

## Baselines atuais

- v0.4.13-local-run-command-0.2.1
- v0.4.14-confirm-send-before-ack

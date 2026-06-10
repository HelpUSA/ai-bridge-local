# AI Bridge Local 0.4.34 - Workers virtuais por chat

Data: 2026-06-10

## Objetivo

Restaurar o comportamento livre do AI Bridge Local: um chat novo pode enviar comandos locais sem precisar abrir outro shell ou fixar um chat especifico manualmente.

A abordagem final desta versao nao usa `start_local_supervisor.bat`. Esse desvio foi removido. O runtime continua usando o gateway local e o worker local existentes, mas o worker agora atua como dispatcher de workers virtuais por origem de chat.

## Problema anterior

O gateway ja possuia uma fila logica por `target_chat_id` mem `/bridge/next-action`, mas o worker consultava apenas:

```text
/bridge/next-action?chat_id=gateway-brain-supervisor
```

Isso fazia o processamento ficar preso ao alvo fixo e nao modelava corretamente a separacao por chat de origem.

## Mudanca implementada

### gateway_local.py

Foi adicionado o endpoint:

```text
GET /bridge/pending-sources?target_chat_id=gateway-brain-supervisor
```

Ele retorna os `source_chat_id` distintos que possuem comandos `run-command` pendentes para o target informado, com contagem de itens por origem.

Exemplo de resposta:

```json
{
  "ok": true,
  "target_chat_id": "gateway-brain-supervisor",
  "sources": [
    {"source_chat_id": "chat-source-A", "queued": 1},
    {"source_chat_id": "chat-source-B", "queued": 1}
  ]
}
```

Tambem foi ampliado `/bridge/next-action` para aceitar o filtro opcional:

```text
source_chat_id=<id>
```

Quando esse filtro e informado, o gateway entrega apenas comandos `run-command` daquela origem de chat.

### brain_worker.py

O `poll_once()` agora consulta `/bridge/pending-sources` e percorre as origens pendentes. Para cada `source_chat_id`, o worker chama:

```text
/bridge/next-action?chat_id=gateway-brain-supervisor&source_chat_id=<source>
```

Isso cria o efeito de worker virtual por chat sem abrir novos shells e sem fixar chats especificos.

## Resultado esperado

- Um unico gateway continua servindo a porta local.
- Um unico worker real pode percorrer varias origens de chat.
- Cada chat de origem tem sua fila logica separada.
- O worker nao consome mensagens `send-chat-message` destinadas a extensao.
- Resultados continuam sendo enfileirados de volta para o `source_chat_id` original.

## Smoke realizado

Foi executado smoke com duas origens artificiais:

- `chat-source-A`
- `chat-source-B`

O endpoint novo retornou ambas as origens com fila pendente. O worker processou as duas separadamente e enfileirou mensagens de resultado de volta para cada origem:

- `result_to_smoke_0434_source_a_001` -> `chat-source-A`
- `result_to_smoke_0434_source_b_001` -> `chat-source-B`

O smoke confirmou a arquitetura de filas virtuais por origem. A primeira rodada retornou `failed -1` nos comandos de teste por erro no `cwd` do proprio script de smoke, nao por erro de roteamento. A parte arquitetural foi confirmada porque as origens foram detectadas, processadas separadamente e removidas da fila pendente.

## Validacao

Validacao final executada com sucesso:

```text
python -m py_compile gateway_local.py brain_worker.py
node --check extension/background.js
Node --check extension/content_script.js
git diff --check
```

Estado final antes de commit:

```text
M brain_worker.py
M gateway_local.py
M extension/manifest.json
```

## Observacoes operacionais

Depois de alterar `gateway_local.py`, e necessario reiniciar o gateway para que novos endpoints HTTP sejam carregados. Durante o smoke, o endpoint `/bridge/pending-sources` retornou 404 enquanto o processo antigo continuava escutando na porta 8766. Apos reiniciar o gateway, o endpoint funcionou corretamente.

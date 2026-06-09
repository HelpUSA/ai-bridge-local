# AI Bridge Local

Gateway local para comunicação entre chats e execução de comandos.
Versão standalone - sem dependência de Railway ou API cloud.

## Arquitetura

Chat → Extensão Chrome (modo local) → Gateway HTTP (:8766) → SQLite → Worker → Comandos

## Estrutura

- `supervisor.bat` - Entry point
- `gateway_local.py` - Servidor HTTP local
- `brain_worker.py` - Executor de comandos
- `config.yaml` - Configuração
- `scripts/` - Scripts utilitários
- `modules/` - Módulos reutilizáveis
- `docs/` - Documentação

## Uso

1. Execute `supervisor.bat`
2. Configure extensão: `AI_BRIDGE_GATEWAY_BASE_URL=http://127.0.0.1:8766`
3. Envie comandos pelo chat

## Versão

0.1.0 - inicial

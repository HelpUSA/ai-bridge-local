# AI Bridge Local - Local bridge envelope 0.4.66

## Objetivo
Padronizar envelope local para comunicacao entre chats e criar replayer dry-run.

## Arquivos
- scripts/watcher/local_bridge_envelope.py
- scripts/watcher/local_bridge_replay_dry_run.py
- scripts/watcher/smoke_local_bridge_envelope.py

## Regras
- message fica no campo raiz.
- payload.message nao e usado para send-chat-message.
- source_chat_id e target_chat_id sao obrigatorios.
- replay real permanece bloqueado; o modo atual e dry-run.

## Proximos passos
- Integrar local_bridge_envelope.py com local_bridge_store.py.
- Criar ack writer em dry-run.
- Criar painel read-only para inbox/outbox/status.

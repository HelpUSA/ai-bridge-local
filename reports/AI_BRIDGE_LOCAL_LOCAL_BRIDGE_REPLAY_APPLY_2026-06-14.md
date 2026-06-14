# AI Bridge Local - Local bridge replay apply 0.4.69

## Objetivo
Criar replay apply controlado para envelopes locais, com dry-run por padrao.

## Arquivos
- scripts/watcher/local_bridge_replay_apply.py
- scripts/watcher/smoke_local_bridge_replay_apply.py

## Garantias
- Dry-run por padrao.
- Escrita somente com --apply.
- Store precisa estar dentro do repo.
- Envelope precisa ter message no campo raiz e target_chat_id.
- Nao executa comandos externos arbitrarios.

## Proximos passos
- Criar worker local opcional.
- Criar replay de status acked/failed a partir do store.
- Criar painel HTML/local se necessario.

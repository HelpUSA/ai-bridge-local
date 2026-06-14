# AI Bridge Local - Local bridge worker dry-run 0.4.70

## Objetivo
Criar worker dry-run para planejar entrega de mensagens do outbox sem executar envio real.

## Arquivos
- scripts/watcher/local_bridge_worker_dry_run.py
- scripts/watcher/smoke_local_bridge_worker_dry_run.py

## Garantias
- Worker e somente planejamento.
- Nao executa comandos externos arbitrarios.
- Nao altera store.
- Conta candidatos e itens enviaveis a partir de outbox/status.

## Proximos passos
- Criar worker apply controlado somente depois de aprovacao explicita.
- Criar limpeza read-only de outbox/status.
- Consolidar roadmap local bridge 0.4.65 a 0.4.70.

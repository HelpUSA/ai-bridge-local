# AI Bridge Local - Local bridge writer and ack 0.4.67

## Objetivo
Integrar envelope local ao store e criar writer de ack/status controlado.

## Arquivos
- scripts/watcher/local_bridge_writer.py
- scripts/watcher/local_bridge_ack_writer.py
- scripts/watcher/smoke_local_bridge_writer_ack.py

## Garantias
- Dry-run por padrao.
- Escrita apenas com --apply e path dentro do repo.
- Smoke usa temp/local_bridge_writer_ack_smoke e remove ao final.
- Nao executa comandos externos arbitrarios.

## Proximos passos
- Criar painel read-only para visualizar store.
- Adicionar replay apply controlado depois de aprovacao explicita.
- Criar worker local opcional.

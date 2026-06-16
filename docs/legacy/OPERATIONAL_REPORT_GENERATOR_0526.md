# Operational report generator 0.5.26

Objetivo: gerar relatorio operacional readonly consolidando versao, tag, commit, validacoes, resumo diagnostico e saude de fila/worker.

## Escopo

- Gera texto markdown.
- Usa dados ja fornecidos por snapshots readonly.
- Nao envia mensagens.
- Nao altera fila.
- Nao executa entrega inter-chat.

## Arquivo principal

- scripts/watcher/operational_report_generator.py
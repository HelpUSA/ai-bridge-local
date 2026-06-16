# Queue worker health 0.5.25

Objetivo: criar health check readonly para fila e worker.

## Cobertura

- Total de comandos.
- Comandos por status.
- Total de workers.
- Quantidade de workers ativos.
- Deteccao de workers ativos duplicados.
- Deteccao de locks stale.
- Alertas readonly.

## Escopo

O health check usa snapshots existentes.
Ele nao altera fila.
Ele nao cria locks.
Ele nao encerra workers.
Ele nao executa entrega inter-chat.
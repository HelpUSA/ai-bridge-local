# AI Bridge Local - Autonomous evolution task queue 0.4.95

## Objetivo
Definir uma fila operacional para ciclos pequenos de evolucao autonoma do repo via watcher.

## Estados da fila
- proposed: ideia registrada, ainda sem execucao.
- triaged: risco e escopo classificados.
- approved: pronto para execucao controlada.
- running: comando watcher em andamento.
- validated: smoke, docs, version_alignment e release_check passaram.
- published: commit, tag e push concluidos.
- audited: audit final read-only confirmou HEAD, tag, versao e guia.
- blocked: item parado por risco, falha ou falta de aprovacao.
- rolled_back: mudanca revertida com registro do motivo.

## Regras
- Um item deve ser pequeno e reversivel.
- Cada item deve declarar objetivo, risco, arquivos tocados, checks e rollback.
- Mudancas destructive ou data_cleanup exigem aprovacao explicita.
- Itens blocked nao devem ser repetidos sem nova proposta minima.
- Itens published precisam de audit final read-only.

## Resultado esperado
A IA passa a organizar a propria evolucao por uma fila auditavel, evitando saltos grandes e mudancas nao rastreadas.

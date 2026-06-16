# AI Bridge Local - Autonomous evolution audit ledger 0.4.96

## Objetivo
Definir um ledger auditavel para registrar cada ciclo de evolucao autonoma do repo via watcher.

## Campos obrigatorios
- task_id: identificador curto e unico do item.
- state: proposed, triaged, approved, running, validated, published, audited, blocked ou rolled_back.
- objective: objetivo pequeno e reversivel.
- risk_class: read_only, docs_only, low_risk_code, mutating_runtime, data_cleanup ou destructive.
- files_touched: lista de arquivos previstos e reais.
- approval_required: sim ou nao.
- approval_reference: referencia da aprovacao quando exigida.
- watcher_command_id: comando watcher usado.
- validation_evidence: smokes, release_check e diff_check.
- publication_evidence: commit, tag e push.
- final_audit_evidence: HEAD, tag, VERSION, guia e smokes.
- rollback_plan: plano minimo de reversao.

## Regras
- Nenhum item pode ir para published sem validation_evidence.
- Nenhum item pode ir para audited sem final_audit_evidence.
- Itens destructive ou data_cleanup exigem approval_reference.
- Itens blocked exigem motivo e proxima acao segura.
- O ledger deve favorecer comandos pequenos e rastreaveis.

## Resultado esperado
Cada evolucao autonoma fica rastreavel do objetivo ao audit final, permitindo revisao, rollback e aprendizado.

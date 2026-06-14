from pathlib import Path
doc = Path('docs/AUTONOMOUS_EVOLUTION_AUDIT_LEDGER.md').read_text(encoding='utf-8')
report = Path('reports/AI_BRIDGE_LOCAL_AUTONOMOUS_EVOLUTION_AUDIT_LEDGER_2026-06-14.md').read_text(encoding='utf-8')
for term in ['task_id', 'state', 'risk_class', 'watcher_command_id', 'validation_evidence', 'publication_evidence', 'final_audit_evidence', 'rollback_plan']:
 assert term in doc
assert 'approval_reference' in doc
assert 'published sem validation_evidence' in doc
assert 'Nao altera runtime' in report
print('OK autonomous_evolution_audit_ledger_smoke')

from pathlib import Path
doc = Path('docs/AUTONOMOUS_CHANGE_PROPOSAL_TEMPLATE.md').read_text(encoding='utf-8')
report = Path('reports/AI_BRIDGE_LOCAL_AUTONOMOUS_CHANGE_PROPOSAL_TEMPLATE_2026-06-14.md').read_text(encoding='utf-8')
for term in ['Contexto atual', 'Problema', 'Escopo', 'Risco', 'Plano dry-run', 'Plano de teste', 'Rollback', 'Audit final']:
 assert term in doc
assert 'git diff --check' in doc
assert 'aprovacao explicita' in doc
assert 'Nao altera runtime' in report
print('OK autonomous_change_proposal_template_smoke')

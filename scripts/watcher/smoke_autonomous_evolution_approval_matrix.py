from pathlib import Path
doc = Path('docs/AUTONOMOUS_EVOLUTION_APPROVAL_MATRIX.md').read_text(encoding='utf-8')
report = Path('reports/AI_BRIDGE_LOCAL_AUTONOMOUS_EVOLUTION_APPROVAL_MATRIX_2026-06-14.md').read_text(encoding='utf-8')
for term in ['read_only', 'docs_only', 'low_risk_code', 'mutating_runtime', 'data_cleanup', 'destructive']:
 assert term in doc
assert 'aprovacao explicita' in doc
assert 'git diff --check' in doc
assert 'Nao altera runtime' in report
print('OK autonomous_evolution_approval_matrix_smoke')

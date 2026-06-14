from pathlib import Path
doc = Path('docs/QUEUE_TRIAGE_PLAYBOOK.md').read_text(encoding='utf-8')
report = Path('reports/AI_BRIDGE_LOCAL_QUEUE_TRIAGE_PLAYBOOK_2026-06-14.md').read_text(encoding='utf-8')
assert 'Nunca limpar' in doc
assert 'queue_health_audit' in doc
assert 'dry-run' in doc
assert 'Nao altera banco' in report
print('OK queue_triage_playbook_smoke')

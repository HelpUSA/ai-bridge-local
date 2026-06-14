from pathlib import Path
doc = Path('docs/AUTONOMOUS_EVOLUTION_TASK_QUEUE.md').read_text(encoding='utf-8')
report = Path('reports/AI_BRIDGE_LOCAL_AUTONOMOUS_EVOLUTION_TASK_QUEUE_2026-06-14.md').read_text(encoding='utf-8')
for term in ['proposed', 'triaged', 'approved', 'running', 'validated', 'published', 'audited', 'blocked', 'rolled_back']:
 assert term in doc
assert 'audit final read-only' in doc
assert 'aprovacao explicita' in doc
assert 'Nao altera runtime' in report
print('OK autonomous_evolution_task_queue_smoke')

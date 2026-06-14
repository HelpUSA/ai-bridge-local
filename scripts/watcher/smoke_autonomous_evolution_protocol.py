from pathlib import Path
doc = Path('docs/AUTONOMOUS_EVOLUTION_PROTOCOL.md').read_text(encoding='utf-8')
report = Path('reports/AI_BRIDGE_LOCAL_AUTONOMOUS_EVOLUTION_PROTOCOL_2026-06-14.md').read_text(encoding='utf-8')
for term in ['governance dry-run', 'release_check', 'audit final read-only', 'Base64', 'Sem alteracao destrutiva implicita']:
 assert term in doc
assert 'evolucao autonoma controlada' in report
assert 'Nao altera runtime' in report
print('OK autonomous_evolution_protocol_smoke')

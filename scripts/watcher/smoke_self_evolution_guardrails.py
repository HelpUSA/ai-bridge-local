from pathlib import Path
doc = Path('docs/SELF_EVOLUTION_GUARDRAILS.md').read_text(encoding='utf-8')
report = Path('reports/AI_BRIDGE_LOCAL_SELF_EVOLUTION_GUARDRAILS_2026-06-14.md').read_text(encoding='utf-8')
for term in ['diagnostico', 'dry-run', 'release_check', 'audit final read-only', 'Nunca expor segredos', 'snapshot']:
 assert term in doc
assert 'Nao ativa automacao autonoma nova' in report
print('OK self_evolution_guardrails_smoke')

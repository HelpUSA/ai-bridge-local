from pathlib import Path
doc = Path('docs/SAFE_ENVELOPE_TEMPLATES.md').read_text(encoding='utf-8')
report = Path('reports/AI_BRIDGE_LOCAL_SAFE_ENVELOPE_TEMPLATES_2026-06-14.md').read_text(encoding='utf-8')
assert 'Preferir blocos pequenos' in doc
assert 'Evitar python -c' in doc
assert 'Usar Base64' in doc
assert 'Auditoria final read-only' in report
print('OK safe_envelope_templates_smoke')

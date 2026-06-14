from pathlib import Path
doc = Path('docs/RELEASE_SAFETY_CHECKLIST.md').read_text(encoding='utf-8')
report = Path('reports/AI_BRIDGE_LOCAL_RELEASE_SAFETY_CHECKLIST_2026-06-14.md').read_text(encoding='utf-8')
assert 'Confirmar arvore limpa' in doc
assert 'Rodar release_check' in doc
assert 'audit final read-only' in doc
assert 'Base64' in doc
assert 'releases seguras' in report
print('OK release_safety_checklist_smoke')

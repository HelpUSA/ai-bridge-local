from pathlib import Path
root = Path(__file__).resolve().parents[2]
text = (root / 'extension' / 'content_script.js').read_text(encoding='utf-8')
assert 'function collectSubmitDiagnostics' in text
assert 'send_button_not_found' in text
assert 'send_button_disabled_or_blocked' in text
assert 'diagnostics: diagnostic' in text
assert 'diagnostic.reason' in text
print('OK delivery_diagnostics_smoke')

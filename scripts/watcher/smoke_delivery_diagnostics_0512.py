from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION = (ROOT / 'VERSION').read_text(encoding='utf-8-sig').strip()
GUIDE = (ROOT / 'docs' / 'AI_BRIDGE_LOCAL_GUIDE.md').read_text(encoding='utf-8-sig')
DOC = (ROOT / 'docs' / 'DELIVERY_DIAGNOSTICS_0512.md').read_text(encoding='utf-8-sig')

REQUIRED_TERMS = [
    'target_chat_not_registered',
    'target_tab_not_open',
    'composer_not_found',
    'modal_blocking',
    'send_button_disabled',
    'inject_timeout',
    'submit_not_confirmed',
]

def version_tuple(value):
    return tuple(int(part) for part in value.split('.'))

assert version_tuple(VERSION) >= version_tuple('0.5.12'), VERSION
assert 'Version alignment 0.5.12' in GUIDE
assert 'Delivery diagnostics 0.5.12' in GUIDE
assert 'v0.5.12-delivery-diagnostics' in GUIDE
for term in REQUIRED_TERMS:
    assert term in DOC, term
assert 'nao executa entrega inter-chat' in DOC
print('OK delivery_diagnostics_0512 ' + VERSION)
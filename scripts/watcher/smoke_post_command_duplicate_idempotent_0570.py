from pathlib import Path
import re

bg = Path('extension/background.js').read_text(encoding='utf-8', errors='replace')
post_start = bg.find('async function postCommand(cmd)')
route_start = bg.find('async function routeBridgeCommand')
assert post_start >= 0
assert route_start > post_start
post_body = bg[post_start:route_start]
dq = chr(34)
assert 'const VERSION = ' + dq + '0.5.70' + dq + ';' in bg
assert 'errorText === ' + dq + 'duplicate' + dq in post_body
assert 'already_queued: true' in post_body
assert 'idempotent: true' in post_body
assert 'throw e;' in post_body
duplicate_idx = post_body.find('errorText === ' + dq + 'duplicate' + dq)
already_idx = post_body.find('already_queued: true')
idempotent_idx = post_body.find('idempotent: true')
throw_idx = post_body.rfind('throw e;')
assert duplicate_idx >= 0
assert duplicate_idx < already_idx < throw_idx
assert duplicate_idx < idempotent_idx < throw_idx
bad_patterns = [
 'errorText === ' + dq + 'inject_timeout' + dq,
 'errorText == ' + dq + 'inject_timeout' + dq,
 'errorText.includes(' + dq + 'inject_timeout' + dq + ')',
 'already_queued: true, error: ' + dq + 'inject_timeout' + dq,
]
for bad in bad_patterns:
 assert bad not in post_body
assert 'routeBridgeCommand(validation.envelope, ' + dq + 'capturedEnvelope' + dq + ')' in bg
assert 'postCommand(validation.envelope)' not in bg
print('OK smoke_post_command_duplicate_idempotent_0570')

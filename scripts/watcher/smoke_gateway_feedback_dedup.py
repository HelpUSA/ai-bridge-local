import pathlib

gateway = pathlib.Path('gateway_local.py').read_text(encoding='utf-8')

assert 'def open_db' in gateway
assert 'PRAGMA busy_timeout = 30000' in gateway
assert 'conn = open_db()' in gateway
assert '[AI_LOCAL_RUN]' in gateway
assert 'result_is_final=1' in gateway
assert 'chat_can_continue=1' in gateway
assert 'next_action=' in gateway

print('OK smoke_gateway_feedback_dedup')

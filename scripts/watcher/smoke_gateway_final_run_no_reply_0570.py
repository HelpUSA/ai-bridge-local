from pathlib import Path
text=Path('gateway_local.py').read_text(encoding='utf-8', errors='replace')
idx=text.index('[AI_LOCAL_RUN]')
block=text[idx:idx+700]
assert 'result_is_final=1' in block
assert 'chat_can_continue=1' in block
assert 'no_reply=0' in block
assert 'no_reply=1' not in block
assert 'fix_run_command_routing' in block
assert 'status=queued' in text
queued_idx=text.index('status=queued')
queued_block=text[queued_idx-250:queued_idx+250]
assert 'no_reply=1' in queued_block
print('OK smoke_gateway_final_run_no_reply_0570')

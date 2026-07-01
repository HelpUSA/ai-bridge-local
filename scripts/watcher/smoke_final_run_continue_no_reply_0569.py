from pathlib import Path
q=chr(34)
bs=chr(92)
text=Path('brain_worker.py').read_text(encoding='utf-8', errors='replace')
start=text.index('def format_result_message')
end=text.index('def enqueue_result_message')
section=text[start:end]
assert '[AI_LOCAL_RUN]' in section
assert 'result_is_final=1' in section
assert 'chat_can_continue = '+q+'1'+q in section
assert 'final_no_reply = '+q+'0'+q+' if chat_can_continue == '+q+'1'+q+' else '+q+'1'+q in section
assert 'f'+q+'no_reply={final_no_reply}'+bs+'n'+q in section
assert q+'no_reply=1'+bs+'n'+q not in section
assert 'no_reply={no_reply}' not in section
print('OK smoke_final_run_continue_no_reply_0569')

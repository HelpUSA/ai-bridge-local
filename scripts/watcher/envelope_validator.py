import json,sys
def die(m): print('INVALID '+m); raise SystemExit(1)
raw=sys.stdin.read().strip()
if raw.startswith('@@'): raw=''.join([x for x in raw.splitlines() if not x.startswith('@@')])
env=json.loads(raw)
for k in ['command_id','source_chat_id','target_chat_id','action','delivery_kind']:
 if k not in env: die('missing '+k)
if env['action']=='send-chat-message':
 if env['delivery_kind']!='inter_agent_message': die('bad delivery kind')
 if not isinstance(env.get('message'),str): die('missing top message')
elif env['action']=='run-command':
 if env['delivery_kind']!='local_capability': die('bad delivery kind')
 if env['target_chat_id']!='gateway-brain-supervisor': die('bad target')
 if not isinstance(env.get('payload'),dict): die('missing payload')
else: die('bad action')
print('VALID')

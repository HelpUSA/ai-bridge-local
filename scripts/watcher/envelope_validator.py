import json,sys
raw=sys.stdin.read().strip()
if raw.startswith('@@'): raw=''.join([x for x in raw.splitlines() if not x.startswith('@@')])
env=json.loads(raw)
need=['schema','schema_version','command_id','source_chat_id','target_chat_id','action','delivery_kind']
miss=[k for k in need if k not in env]
assert not miss, miss
assert env['schema']=='ai_bridge_local.envelope'
if env['action']=='send-chat-message': assert env['delivery_kind']=='inter_agent_message' and isinstance(env.get('message'),str)
elif env['action']=='run-command': assert env['delivery_kind']=='local_capability' and env['target_chat_id']=='gateway-brain-supervisor' and isinstance(env.get('payload'),dict)
else: raise SystemExit(1)
print('VALID')

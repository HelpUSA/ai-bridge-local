import argparse,json,time
p=argparse.ArgumentParser()
p.add_argument('--source',required=True)
p.add_argument('--target',required=True)
p.add_argument('--action',required=True,choices=['send-chat-message','run-command'])
p.add_argument('--id',default='cmd_'+str(int(time.time())))
p.add_argument('--message',default='')
p.add_argument('--cwd',default='D:/dev/autocode/ai-bridge-local')
p.add_argument('--timeout',type=int,default=120)
p.add_argument('--command',nargs='*')
a,rest=p.parse_known_args()
cmd=(a.command or [])+rest
env={'schema':'ai_bridge_local.envelope','schema_version':1,'command_id':a.id,'source_chat_id':a.source,'target_chat_id':a.target,'action':a.action,'conversation_id':'ai_bridge_local_builder','from_agent':'command_builder'}
if a.action=='send-chat-message' and not a.message: raise SystemExit('message required')
if a.action=='run-command' and a.target!='gateway-brain-supervisor': raise SystemExit('bad target')
if a.action=='send-chat-message': env.update({'delivery_kind':'inter_agent_message','message':a.message})
if a.action=='run-command': env.update({'delivery_kind':'local_capability','payload':{'cwd':a.cwd,'timeout_seconds':a.timeout,'command':cmd or ['git','status','-sb']}})
print('@@'+'AI_BRIDGE_LOCAL_START@@')
print(json.dumps(env,separators=(',', ':')))
print('@@'+'AI_BRIDGE_LOCAL_END@@')


import argparse,json,time
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--source',required=True)
 p.add_argument('--target',required=True)
 p.add_argument('--action',required=True,choices=['send-chat-message','run-command'])
 p.add_argument('--id',default='cmd_'+str(int(time.time())))
 p.add_argument('--message',default='')
 p.add_argument('--cwd',default='D:/dev/autocode/ai-bridge-local')
 p.add_argument('--timeout',type=int,default=120)
 p.add_argument('--command',nargs='*')
 a=p.parse_args()
 env={'command_id':a.id,'source_chat_id':a.source,'target_chat_id':a.target,'action':a.action,'conversation_id':'ai_bridge_local_builder','from_agent':'command_builder'}
 if a.action=='send-chat-message':
 if not a.message: raise SystemExit('message required')
 env['delivery_kind']='inter_agent_message'
 env['message']=a.message
 else:
 if a.target!='gateway-brain-supervisor': raise SystemExit('bad target')
 env['delivery_kind']='local_capability'
 env['payload']={'cwd':a.cwd,'timeout_seconds':a.timeout,'command':a.command or ['git','status','-sb']}
 print('@@'+'AI_BRIDGE_LOCAL_START@@')
 print(json.dumps(env,separators=(',', ':')))
 print('@@'+'AI_BRIDGE_LOCAL_END@@')
if name=='main': main()

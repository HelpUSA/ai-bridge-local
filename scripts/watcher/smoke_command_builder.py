import subprocess,sys
from pathlib import Path
ROOT=Path.cwd()
b=ROOT/'scripts'/'watcher'/'command_builder.py'
v=ROOT/'scripts'/'watcher'/'envelope_validator.py'
def build(args): return subprocess.check_output([sys.executable,str(b)]+args,cwd=ROOT,text=True,encoding='utf-8')
def valid(raw):
 p=subprocess.run([sys.executable,str(v)],input=raw,cwd=ROOT,text=True,encoding='utf-8',capture_output=True)
 assert p.returncode==0,p.stdout+p.stderr
raw=build(['--id','smoke-run-command-builder','--source','source-chat','--target','gateway-brain-supervisor','--action','run-command','--cwd','D:/dev/autocode/ai-bridge-local','--timeout','30','--command','git','status'])
assert '@@AI_BRIDGE_LOCAL_START@@' in raw and 'local_capability' in raw and 'gateway-brain-supervisor' in raw
valid(raw)
raw=build(['--id','smoke-send-command-builder','--source','source-chat','--target','target-chat','--action','send-chat-message','--message','hello'])
assert 'inter_agent_message' in raw and 'hello' in raw
valid(raw)
print('OK command_builder_smoke')

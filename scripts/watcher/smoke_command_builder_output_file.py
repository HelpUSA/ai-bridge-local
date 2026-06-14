import json,subprocess,sys
from pathlib import Path
out=Path('temp/builder_envelopes/smoke_output_file.txt')
cp=subprocess.run([sys.executable,'scripts/watcher/command_builder.py','--source','source-chat','--target','gateway-brain-supervisor','--action','run-command','--id','smoke_builder_output_file','--output-file',str(out),'--command','git','status','-sb'],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
assert cp.stdout == ''
raw=out.read_text(encoding='utf-8')
assert '@@AI_BRIDGE_LOCAL_START@@' in raw
body=''.join(line for line in raw.splitlines() if not line.startswith('@@'))
env=json.loads(body)
assert env['command_id']=='smoke_builder_output_file'
assert env['payload']['command']==['git','status','-sb']
print('OK command_builder_output_file_smoke')

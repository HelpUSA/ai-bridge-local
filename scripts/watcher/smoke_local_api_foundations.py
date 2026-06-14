import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
ro = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_api_readonly.py'), '--path', 'VERSION'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
dry = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_api_dry_run.py'), '--intent', 'run_command_dry_run'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
chat = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'chat_bridge_plan.py')], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
items = [json.loads(ro.stdout), json.loads(dry.stdout), json.loads(chat.stdout)]
assert items[0]['schema'] == 'ai_bridge_local.local_api_readonly'
assert items[1]['schema'] == 'ai_bridge_local.local_api_dry_run'
assert items[2]['schema'] == 'ai_bridge_local.chat_bridge_plan'
assert all(item['executes_commands'] is False for item in items)
assert items[0]['allowed'] is True
assert items[1]['intent_allowed'] is True
assert items[2]['extension_dependency'] == 'optional after local API exists'
print('OK local_api_foundations_smoke')

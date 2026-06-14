import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
SCRIPT = ROOT / 'scripts' / 'watcher' / 'auditor_mode.py'
run = subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
assert 'AI_BRIDGE_LOCAL_AUDIT' in run.stdout
assert 'Executes commands: no' in run.stdout
assert 'git_status_clean' in run.stdout
js = subprocess.run([sys.executable, str(SCRIPT), '--json'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
data = json.loads(js.stdout)
assert data['schema'] == 'ai_bridge_local.auditor_mode'
assert data['schema_version'] == 1
assert data['executes_commands'] is False
assert data['version']
assert len(data['checks']) >= 5
assert 'git_status_clean' in [item['name'] for item in data['checks']]
print('OK auditor_mode_smoke')

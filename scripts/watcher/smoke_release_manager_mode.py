import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
SCRIPT = ROOT / 'scripts' / 'watcher' / 'release_manager_mode.py'
run = subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
assert 'AI_BRIDGE_LOCAL_RELEASE_MANAGER_PLAN' in run.stdout
assert 'Executes commands: no' in run.stdout
assert 'v0.4.62-release-manager-mode' in run.stdout
js = subprocess.run([sys.executable, str(SCRIPT), '--json'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
data = json.loads(js.stdout)
assert data['schema'] == 'ai_bridge_local.release_manager_mode'
assert data['schema_version'] == 1
assert data['executes_commands'] is False
assert data['target_version'] == '0.4.62'
assert data['tag_name'] == 'v0.4.62-release-manager-mode'
assert len(data['steps']) >= 8
assert 'tag the same HEAD commit' in data['steps']
print('OK release_manager_mode_smoke')

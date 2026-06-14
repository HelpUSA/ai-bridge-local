import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
SCRIPT = ROOT / 'scripts' / 'watcher' / 'planner_mode.py'
run = subprocess.run([sys.executable, str(SCRIPT), '--objective', 'ship planner mode', '--repo', 'D:/dev/autocode/ai-bridge-local'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
assert 'AI_BRIDGE_LOCAL_PLAN' in run.stdout
assert 'Executes commands: no' in run.stdout
assert 'Requires approval: yes' in run.stdout
assert 'INSPECT' in run.stdout
assert 'AUDIT' in run.stdout
js = subprocess.run([sys.executable, str(SCRIPT), '--objective', 'ship planner mode', '--json'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
data = json.loads(js.stdout)
assert data['schema'] == 'ai_bridge_local.planner_mode'
assert data['schema_version'] == 1
assert data['executes_commands'] is False
assert data['requires_approval'] is True
assert len(data['phases']) == 4
assert data['phases'][0]['name'] == 'inspect'
bad = subprocess.run([sys.executable, str(SCRIPT), '--objective', ''], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert bad.returncode != 0
print('OK planner_mode_smoke')

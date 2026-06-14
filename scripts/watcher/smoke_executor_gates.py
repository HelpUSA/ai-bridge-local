import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
SCRIPT = ROOT / 'scripts' / 'watcher' / 'executor_gates.py'
blocked = subprocess.run([sys.executable, str(SCRIPT), '--intent', 'apply approved patch'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
assert 'Allowed to execute: false' in blocked.stdout
allowed = subprocess.run([sys.executable, str(SCRIPT), '--intent', 'apply approved patch', '--approved', '--json'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
data = json.loads(allowed.stdout)
assert data['schema'] == 'ai_bridge_local.executor_gates'
assert data['schema_version'] == 1
assert data['executes_commands'] is False
assert data['approved'] is True
assert data['allowed_to_execute'] is True
assert len(data['gates']) == 4
assert data['gates'][0]['name'] == 'approval'
bad = subprocess.run([sys.executable, str(SCRIPT), '--intent', ''], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert bad.returncode != 0
print('OK executor_gates_smoke')

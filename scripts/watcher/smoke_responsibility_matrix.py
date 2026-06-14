import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
SCRIPT = ROOT / 'scripts' / 'watcher' / 'responsibility_matrix.py'
run = subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
data = json.loads(run.stdout)
assert data['schema'] == 'ai_bridge_local.responsibility_matrix'
assert data['schema_version'] == 1
roles = {item['role']: item for item in data['roles']}
for role in ['supervisor', 'executor', 'fiscal', 'documentador']:
 assert role in roles
assert roles['executor']['may_execute'] is True
assert roles['supervisor']['may_execute'] is False
assert 'evidence' in roles['executor']['responsibility']
assert 'validate evidence' in roles['fiscal']['responsibility']
print('OK responsibility_matrix_smoke')

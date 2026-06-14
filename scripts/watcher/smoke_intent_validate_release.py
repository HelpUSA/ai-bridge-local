import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
cp = subprocess.run([sys.executable, str(ROOT / 'scripts/watcher/command_intake.py'), '--intent', 'validate_release', '--cwd', '.', '--command-id', 'smoke_validate_release_plan'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert cp.returncode == 0, cp.stderr
plan = json.loads(cp.stdout)
assert plan['schema'] == 'ai_bridge_local.command_intake_plan', plan
assert plan['intent'] == 'validate_release', plan
assert plan['risk'] == 'validation', plan
assert plan['status'] == 'planned', plan
assert plan['steps'][0]['command'][0] == 'powershell', plan
assert plan['steps'][0]['command'][-1] == 'scripts/watcher/release_check.ps1', plan
print('OK validate_release_intent_smoke')

import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
cmd = [sys.executable, str(ROOT / 'scripts' / 'watcher' / 'governance_risk_classifier.py')]
read = subprocess.run(cmd + ['--command', 'git status -sb'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
mut = subprocess.run(cmd + ['--command', 'git commit -m test'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
des = subprocess.run(cmd + ['--command', 'Remove-Item temp -Recurse -Force'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
items = [json.loads(read.stdout), json.loads(mut.stdout), json.loads(des.stdout)]
assert items[0]['schema'] == 'ai_bridge_local.governance_risk_classifier'
assert items[0]['executes_commands'] is False
assert items[0]['risk_level'] == 'read_only_or_dry_run'
assert items[1]['risk_level'] == 'mutating'
assert items[2]['risk_level'] == 'destructive'
print('OK governance_risk_classifier_smoke')

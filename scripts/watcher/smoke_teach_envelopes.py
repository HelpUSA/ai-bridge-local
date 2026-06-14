import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
SCRIPT = ROOT / 'scripts' / 'watcher' / 'teach_envelopes.py'
run = subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
assert 'teach_watcher_basics' in run.stdout
assert 'teach_repo_safety' in run.stdout
assert 'teach_release_flow' in run.stdout
assert 'teach_failure_recovery' in run.stdout
assert 'Use strict JSON envelope markers' in run.stdout
assert 'Run smokes and release_check' in run.stdout
js = subprocess.run([sys.executable, str(SCRIPT), 'teach_release_flow', '--json'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
data = json.loads(js.stdout)
assert data['schema'] == 'ai_bridge_local.teach_envelopes'
assert data['schema_version'] == 1
assert list(data['lessons'].keys()) == ['teach_release_flow']
assert 'Tag release commit' in data['lessons']['teach_release_flow']['steps']
bad = subprocess.run([sys.executable, str(SCRIPT), 'missing_lesson'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert bad.returncode != 0
assert 'unknown lesson' in bad.stderr or 'unknown lesson' in bad.stdout
print('OK teach_envelopes_smoke')

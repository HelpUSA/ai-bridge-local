import json
import subprocess
import sys
import tempfile
from pathlib import Path
ROOT = Path.cwd()
log = Path(tempfile.mkdtemp()) / 'decisions.jsonl'
cmd = [sys.executable, str(ROOT / 'scripts' / 'watcher' / 'governance_decision_log.py'), '--log-file', str(log)]
subprocess.run(cmd + ['--command-id', 'read', '--command', 'git', 'status', '-sb'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
subprocess.run(cmd + ['--command-id', 'danger', '--command', 'Remove-Item', 'temp', '-Recurse', '-Force'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
items = [json.loads(x) for x in log.read_text(encoding='utf-8').splitlines()]
assert len(items) == 2
assert items[0]['risk_level'] == 'read_only_or_dry_run'
assert items[1]['risk_level'] == 'destructive'
assert items[1]['requires_manual_review'] is True
print('OK governance_decision_log_smoke')

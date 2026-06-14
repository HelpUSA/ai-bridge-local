import json
import subprocess
import sys
import tempfile
from pathlib import Path
ROOT = Path.cwd()
log = Path(tempfile.mkdtemp()) / 'decisions.jsonl'
logger = [sys.executable, str(ROOT / 'scripts' / 'watcher' / 'governance_decision_log.py'), '--log-file', str(log)]
subprocess.run(logger + ['--command-id', 'read', '--command', 'git', 'status', '-sb'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
subprocess.run(logger + ['--command-id', 'mut', '--command', 'git', 'commit', '-m', 'x'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
report = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'governance_risk_report.py'), '--log-file', str(log)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
payload = json.loads(report.stdout)
assert payload['schema'] == 'ai_bridge_local.governance_risk_report'
assert payload['total'] == 2
assert payload['risk_counts']['read_only_or_dry_run'] == 1
assert payload['risk_counts']['mutating'] == 1
assert payload['requires_manual_review'] == 1
print('OK governance_risk_report_smoke')

import json
import shutil
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
tmp = ROOT / 'temp' / 'local_bridge_worker_dry_run_smoke'
shutil.rmtree(tmp, ignore_errors=True)
tmp.mkdir(parents=True, exist_ok=True)
subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_writer.py'), '--store-dir', str(tmp), '--from-chat', 'a', '--to-chat', 'b', '--message', 'worker', '--apply'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
worker = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_worker_dry_run.py'), '--store-dir', str(tmp)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
dash = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_dashboard.py'), '--store-dir', str(tmp)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
w = json.loads(worker.stdout)
d = json.loads(dash.stdout)
assert w['schema'] == 'ai_bridge_local.local_bridge_worker_dry_run'
assert w['executes_commands'] is False
assert w['dry_run'] is True
assert w['candidate_count'] >= 1
assert w['sendable_count'] >= 1
assert d['counts']['outbox'] >= 1
shutil.rmtree(tmp, ignore_errors=True)
print('OK local_bridge_worker_dry_run_smoke')

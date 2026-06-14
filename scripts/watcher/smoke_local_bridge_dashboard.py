import json
import shutil
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
tmp = ROOT / 'temp' / 'local_bridge_dashboard_smoke'
shutil.rmtree(tmp, ignore_errors=True)
tmp.mkdir(parents=True, exist_ok=True)
subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_writer.py'), '--store-dir', str(tmp), '--from-chat', 'a', '--to-chat', 'b', '--message', 'dashboard', '--apply'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_ack_writer.py'), '--store-dir', str(tmp), '--message-id', 'm1', '--status', 'acked', '--apply'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
dash = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_dashboard.py'), '--store-dir', str(tmp)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
summary = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_dashboard_summary.py'), '--store-dir', str(tmp)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
data = json.loads(dash.stdout)
assert data['schema'] == 'ai_bridge_local.local_bridge_dashboard'
assert data['executes_commands'] is False
assert data['counts']['outbox'] >= 1
assert data['counts']['status'] >= 2
assert 'AI_BRIDGE_LOCAL_BRIDGE_DASHBOARD' in summary.stdout
assert 'Executes commands: no' in summary.stdout
shutil.rmtree(tmp, ignore_errors=True)
print('OK local_bridge_dashboard_smoke')

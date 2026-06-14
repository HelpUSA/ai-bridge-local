import json
import shutil
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
tmp = ROOT / 'temp' / 'local_bridge_store_smoke'
shutil.rmtree(tmp, ignore_errors=True)
tmp.mkdir(parents=True, exist_ok=True)
status = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_store.py'), '--store-dir', str(tmp), '--action', 'status'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
dry = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_store.py'), '--store-dir', str(tmp), '--action', 'enqueue', '--message', 'dry message'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
applied = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_store.py'), '--store-dir', str(tmp), '--action', 'enqueue', '--message', 'real message', '--apply'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
rec = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_reconcile.py'), '--store-dir', str(tmp)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
items = [json.loads(status.stdout), json.loads(dry.stdout), json.loads(applied.stdout), json.loads(rec.stdout)]
assert items[0]['schema'] == 'ai_bridge_local.local_bridge_store'
assert items[1]['dry_run'] is True
assert items[2]['dry_run'] is False
assert items[2]['entry_count'] >= 1
assert items[3]['schema'] == 'ai_bridge_local.local_bridge_reconcile'
assert items[3]['counts']['outbox'] >= 1
assert all(item['executes_commands'] is False for item in items)
shutil.rmtree(tmp, ignore_errors=True)
print('OK local_bridge_store_smoke')

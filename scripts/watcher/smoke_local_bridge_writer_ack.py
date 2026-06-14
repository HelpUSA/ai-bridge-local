import json
import shutil
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
tmp = ROOT / 'temp' / 'local_bridge_writer_ack_smoke'
shutil.rmtree(tmp, ignore_errors=True)
tmp.mkdir(parents=True, exist_ok=True)
dry = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_writer.py'), '--store-dir', str(tmp), '--from-chat', 'a', '--to-chat', 'b', '--message', 'dry'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
applied = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_writer.py'), '--store-dir', str(tmp), '--from-chat', 'a', '--to-chat', 'b', '--message', 'apply', '--apply'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
ack = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_ack_writer.py'), '--store-dir', str(tmp), '--message-id', 'm1', '--status', 'acked', '--apply'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
rec = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_reconcile.py'), '--store-dir', str(tmp)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
items = [json.loads(dry.stdout), json.loads(applied.stdout), json.loads(ack.stdout), json.loads(rec.stdout)]
assert items[0]['schema'] == 'ai_bridge_local.local_bridge_writer'
assert items[0]['dry_run'] is True
assert items[1]['dry_run'] is False
assert items[1]['envelope_valid'] is True
assert items[2]['schema'] == 'ai_bridge_local.local_bridge_ack_writer'
assert items[2]['dry_run'] is False
assert items[3]['counts']['outbox'] >= 1
assert items[3]['counts']['status'] >= 2
assert all(item['executes_commands'] is False for item in items)
shutil.rmtree(tmp, ignore_errors=True)
print('OK local_bridge_writer_ack_smoke')

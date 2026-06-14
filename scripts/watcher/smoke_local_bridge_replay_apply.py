import json
import shutil
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
tmp = ROOT / 'temp' / 'local_bridge_replay_apply_smoke'
shutil.rmtree(tmp, ignore_errors=True)
tmp.mkdir(parents=True, exist_ok=True)
env_file = tmp / 'envelope.json'
built = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_envelope.py'), '--from-chat', 'a', '--to-chat', 'b', '--message', 'replay'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
env_file.write_text(built.stdout, encoding='utf-8')
dry = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_replay_apply.py'), '--envelope-file', str(env_file), '--store-dir', str(tmp)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
applied = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_replay_apply.py'), '--envelope-file', str(env_file), '--store-dir', str(tmp), '--apply'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
rec = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_reconcile.py'), '--store-dir', str(tmp)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
items = [json.loads(dry.stdout), json.loads(applied.stdout), json.loads(rec.stdout)]
assert items[0]['schema'] == 'ai_bridge_local.local_bridge_replay_apply'
assert items[0]['dry_run'] is True
assert items[0]['valid_envelope'] is True
assert items[1]['dry_run'] is False
assert items[1]['outbox_count'] >= 1
assert items[2]['counts']['outbox'] >= 1
assert items[2]['counts']['status'] >= 1
assert all(item['executes_commands'] is False for item in items)
shutil.rmtree(tmp, ignore_errors=True)
print('OK local_bridge_replay_apply_smoke')

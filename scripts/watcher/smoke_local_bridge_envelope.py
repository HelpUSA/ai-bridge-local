import json
import subprocess
import sys
import tempfile
from pathlib import Path
ROOT = Path.cwd()
with tempfile.TemporaryDirectory() as tmp:
 env_file = Path(tmp) / 'envelope.json'
 built = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_envelope.py'), '--from-chat', 'a', '--to-chat', 'b', '--message', 'msg'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
 env_file.write_text(built.stdout, encoding='utf-8')
 replay = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_replay_dry_run.py'), '--envelope-file', str(env_file), '--store-dir', str(Path(tmp) / 'store')], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
 envelope = json.loads(built.stdout)
 plan = json.loads(replay.stdout)
assert envelope['schema'] == 'ai_bridge_local.local_bridge_envelope'
assert envelope['valid'] is True
assert envelope['message'] == 'msg'
assert 'payload' not in envelope
assert plan['schema'] == 'ai_bridge_local.local_bridge_replay_plan'
assert plan['dry_run'] is True
assert plan['envelope_valid'] is True
assert plan['executes_commands'] is False
print('OK local_bridge_envelope_smoke')

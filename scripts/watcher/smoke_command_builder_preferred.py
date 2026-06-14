import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
out = Path(tempfile.mkdtemp()) / 'preferred.txt'
cmd = [
 sys.executable,
 str(ROOT / 'scripts' / 'watcher' / 'command_builder_preferred.py'),
 '--source',
 'src-chat',
 '--target',
 'gateway-brain-supervisor',
 '--action',
 'run-command',
 '--id',
 'preferred-smoke',
 '--cwd',
 '.',
 '--timeout',
 '60',
 '--output-file',
 str(out),
 '--command',
 'git',
 'status',
 '-sb',
]
subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
raw = out.read_text(encoding='utf-8')
body = raw.split('@@AI_BRIDGE_LOCAL_START@@', 1)[1].split('@@AI_BRIDGE_LOCAL_END@@', 1)[0].strip()
env = json.loads(body)
assert env['delivery_kind'] == 'local_capability'
assert env['payload']['command'] == ['git', 'status', '-sb']
assert env['payload']['governance_advisory']['risk_level'] == 'read_only_or_dry_run'
assert env['payload']['governance_advisory']['blocks_execution'] is False
print('OK command_builder_preferred_smoke')

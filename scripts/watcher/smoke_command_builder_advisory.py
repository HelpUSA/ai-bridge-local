import json
import subprocess
import sys
import tempfile
from pathlib import Path
ROOT = Path.cwd()
def run_checked(cmd):
 r = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 assert r.returncode == 0, r.stderr + r.stdout
 return r
out = Path(tempfile.mkdtemp()) / 'advisory_envelope.txt'
cmd = [sys.executable, str(ROOT / 'scripts' / 'watcher' / 'command_builder_advisory.py'), '--source', 'src-chat', '--target', 'gateway-brain-supervisor', '--action', 'run-command', '--id', 'advisory-smoke', '--cwd', '.', '--timeout', '60', '--output-file', str(out), '--command', 'git', 'status', '-sb']
run_checked(cmd)
raw = out.read_text(encoding='utf-8')
body = raw.split('@@AI_BRIDGE_LOCAL_START@@', 1)[1].split('@@AI_BRIDGE_LOCAL_END@@', 1)[0].strip()
env = json.loads(body)
adv = env['payload']['governance_advisory']
assert env['delivery_kind'] == 'local_capability'
assert env['payload']['command'] == ['git', 'status', '-sb']
assert adv['schema'] == 'ai_bridge_local.governance_preflight'
assert adv['executes_commands'] is False
assert adv['blocks_execution'] is False
assert adv['risk_level'] == 'read_only_or_dry_run'
assert adv['requires_manual_review'] is False
out2 = Path(tempfile.mkdtemp()) / 'advisory_mutating_envelope.txt'
cmd2 = [sys.executable, str(ROOT / 'scripts' / 'watcher' / 'command_builder_advisory.py'), '--source', 'src-chat', '--target', 'gateway-brain-supervisor', '--action', 'run-command', '--id', 'advisory-smoke-mut', '--cwd', '.', '--timeout', '60', '--output-file', str(out2), '--command', 'git', 'commit', '-m', 'x']
run_checked(cmd2)
raw2 = out2.read_text(encoding='utf-8')
body2 = raw2.split('@@AI_BRIDGE_LOCAL_START@@', 1)[1].split('@@AI_BRIDGE_LOCAL_END@@', 1)[0].strip()
env2 = json.loads(body2)
adv2 = env2['payload']['governance_advisory']
assert adv2['risk_level'] == 'mutating'
assert adv2['requires_manual_review'] is True
assert adv2['blocks_execution'] is False
print('OK command_builder_advisory_smoke')

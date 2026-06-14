import json
import subprocess
import sys
def load_plan(*args):
 cp = subprocess.run([sys.executable, 'scripts/watcher/command_intake.py', *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
 return json.loads(cp.stdout)
repo = load_plan('--intent', 'inspect_repo', '--command-id', 'smoke_inspect_repo')
assert repo['schema'] == 'ai_bridge_local.command_intake_plan'
assert repo['schema_version'] == 2
assert repo['intent'] == 'inspect_repo'
assert repo['risk'] == 'read_only'
assert repo['status'] == 'planned'
assert repo['steps'][0]['command'] == ['git', 'status', '-sb']
docs = load_plan('--intent', 'inspect_docs', '--command-id', 'smoke_inspect_docs')
assert docs['steps'][1]['command'] == ['python', 'scripts/watcher/smoke_docs.py']
smokes = load_plan('--intent', 'run_smokes', '--command-id', 'smoke_run_smokes')
assert smokes['risk'] == 'validation'
executed = load_plan('--intent', 'run_smokes', '--command-id', 'smoke_execute', '--execute', '--timeout', '120')
assert executed['status'] == 'acked'
assert all(item['return_code'] == 0 for item in executed['results'])
print('OK command_intake_smoke')

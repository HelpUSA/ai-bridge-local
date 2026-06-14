import json
import subprocess
import sys
cp = subprocess.run([sys.executable, 'scripts/watcher/command_intake.py', '--intent', 'inspect_repo', '--command-id', 'smoke_inspect_repo'], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
repo = json.loads(cp.stdout)
assert repo['schema'] == 'ai_bridge_local.command_intake_plan'
assert repo['intent'] == 'inspect_repo'
assert repo['risk'] == 'read_only'
assert repo['status'] == 'planned'
assert repo['steps'][0]['command'] == ['git', 'status', '-sb']
cp = subprocess.run([sys.executable, 'scripts/watcher/command_intake.py', '--intent', 'inspect_docs', '--command-id', 'smoke_inspect_docs'], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
docs = json.loads(cp.stdout)
assert docs['steps'][1]['command'] == ['python', 'scripts/watcher/smoke_docs.py']
cp = subprocess.run([sys.executable, 'scripts/watcher/command_intake.py', '--intent', 'run_smokes', '--command-id', 'smoke_run_smokes'], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
smokes = json.loads(cp.stdout)
assert smokes['risk'] == 'validation'
assert len(smokes['steps']) >= 3
cp = subprocess.run([sys.executable, 'scripts/watcher/command_intake.py', '--intent', 'run_smokes', '--command-id', 'smoke_execute', '--execute', '--timeout', '120'], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
executed = json.loads(cp.stdout)
assert executed['status'] == 'acked'
assert all(item['return_code'] == 0 for item in executed['results'])
print('OK command_intake_smoke')

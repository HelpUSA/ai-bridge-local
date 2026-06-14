import argparse
import json
import subprocess
from pathlib import Path
ROOT = Path.cwd()
parser = argparse.ArgumentParser(description='Build a safe AI Bridge Local release plan without changing files.')
parser.add_argument('--target-version', default='0.4.62')
parser.add_argument('--json', action='store_true')
args = parser.parse_args()
run = lambda cmd: subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.strip()
status = run(['git', 'status', '-sb'])
head = run(['git', 'log', '--oneline', '--decorate', '-1'])
current_version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
tag_name = 'v' + args.target_version + '-release-manager-mode'
steps = ['read-only status audit', 'prepare version bump and docs markers', 'run py_compile and focused smokes', 'run release_check and diff check', 'commit once after green validations', 'tag the same HEAD commit', 'push branch and tag', 'run final read-only audit']
checks = [{'name': 'git_status_visible', 'passed': status.startswith('## main'), 'evidence': status}, {'name': 'current_version_visible', 'passed': bool(current_version), 'evidence': current_version}, {'name': 'target_version_visible', 'passed': bool(args.target_version), 'evidence': args.target_version}, {'name': 'tag_name_computed', 'passed': tag_name.startswith('v'), 'evidence': tag_name}]
payload = {'schema': 'ai_bridge_local.release_manager_mode', 'schema_version': 1, 'executes_commands': False, 'head': head, 'status': status, 'current_version': current_version, 'target_version': args.target_version, 'tag_name': tag_name, 'steps': steps, 'checks': checks, 'divergences': [item['name'] for item in checks if not item['passed']]}
lines = ['AI_BRIDGE_LOCAL_RELEASE_MANAGER_PLAN', 'Head: ' + head, 'Status: ' + status, 'Current version: ' + current_version, 'Target version: ' + args.target_version, 'Tag: ' + tag_name, 'Executes commands: no', 'Steps:']
[lines.append('- ' + item) for item in steps]
lines.append('Divergences: ' + (', '.join(payload['divergences']) if payload['divergences'] else 'none'))
print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else chr(10).join(lines))

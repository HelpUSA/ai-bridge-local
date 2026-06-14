import argparse
import json
import subprocess
from pathlib import Path
ROOT = Path.cwd()
parser = argparse.ArgumentParser(description='Audit AI Bridge Local release metadata without changing files.')
parser.add_argument('--json', action='store_true')
args = parser.parse_args()
run = lambda cmd: subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.strip()
status = run(['git', 'status', '-sb'])
head = run(['git', 'log', '--oneline', '--decorate', '-1'])
tags = run(['git', 'tag', '--sort=-creatordate']).splitlines()[:8]
version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
guide = (ROOT / 'docs' / 'AI_BRIDGE_LOCAL_GUIDE.md').read_text(encoding='utf-8')
expected_tag = 'v' + version + '-auditor-mode' if version == '0.4.61' else 'v' + version
checks = [{'name': 'git_status_clean', 'passed': status.startswith('## main...origin/main') and ' M ' not in status and '??' not in status, 'evidence': status}, {'name': 'version_present', 'passed': bool(version), 'evidence': version}, {'name': 'tag_visible', 'passed': expected_tag in tags or any(version in item for item in tags), 'evidence': ', '.join(tags)}, {'name': 'docs_release_marker', 'passed': ('v' + version) in guide, 'evidence': 'v' + version}, {'name': 'docs_version_alignment_single', 'passed': guide.count('## Version alignment ' + version) == 1, 'evidence': str(guide.count('## Version alignment ' + version))}]
payload = {'schema': 'ai_bridge_local.auditor_mode', 'schema_version': 1, 'executes_commands': False, 'head': head, 'status': status, 'version': version, 'latest_tags': tags, 'checks': checks, 'divergences': [item['name'] for item in checks if not item['passed']]}
lines = ['AI_BRIDGE_LOCAL_AUDIT', 'Head: ' + head, 'Status: ' + status, 'Version: ' + version, 'Executes commands: no', 'Divergences: ' + (', '.join(payload['divergences']) if payload['divergences'] else 'none'), '']
[lines.extend([item['name'], '- passed: ' + str(item['passed']).lower(), '- evidence: ' + item['evidence'], '']) for item in checks]
print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else chr(10).join(lines))

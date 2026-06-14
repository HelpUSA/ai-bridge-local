import json
import subprocess
from pathlib import Path
ROOT = Path.cwd()
run = lambda cmd: subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.strip()
tags = run(['git', 'tag', '--sort=-creatordate']).splitlines()[:12]
head = run(['git', 'log', '--oneline', '--decorate', '-12'])
known_note = 'v0.4.60-executor-gates has a documented post-tag guide reference commit in current history.'
payload = {'schema': 'ai_bridge_local.tag_divergence_report', 'executes_commands': False, 'latest_tags': tags, 'recent_log': head, 'known_notes': [known_note]}
print(json.dumps(payload, ensure_ascii=False, indent=2))

import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
scripts = ['post_release_audit.py', 'tag_divergence_report.py', 'dead_letters_review.py']
outputs = []
[outputs.append(subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / item)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout) for item in scripts]
parsed = [json.loads(item) for item in outputs]
assert parsed[0]['schema'] == 'ai_bridge_local.post_release_audit'
assert parsed[1]['schema'] == 'ai_bridge_local.tag_divergence_report'
assert parsed[2]['schema'] == 'ai_bridge_local.dead_letters_review'
assert all(item['executes_commands'] is False for item in parsed)
print('OK hardening_tools_smoke')

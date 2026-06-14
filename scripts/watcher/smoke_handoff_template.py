import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
SCRIPT = ROOT / 'scripts' / 'watcher' / 'handoff_template.py'
BASE = [sys.executable, str(SCRIPT), '--project', 'AI Bridge Local', '--repo', 'D:/dev/autocode/ai-bridge-local', '--status', 'repo clean and release validated', '--files', 'VERSION,docs/AI_BRIDGE_LOCAL_GUIDE.md', '--validations', 'smoke_docs,release_check,diff_check', '--pending', 'next roadmap item', '--next-command', 'git status -sb']
text = subprocess.run(BASE, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
assert 'AI_BRIDGE_LOCAL_HANDOFF' in text.stdout
assert 'Current status:' in text.stdout
assert 'Files changed:' in text.stdout
assert 'Next safe command:' in text.stdout
assert 'git status -sb' in text.stdout
js = subprocess.run(BASE + ['--json'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
data = json.loads(js.stdout)
assert data['schema'] == 'ai_bridge_local.handoff_template'
assert data['schema_version'] == 1
assert data['project'] == 'AI Bridge Local'
assert data['files_changed'] == ['VERSION', 'docs/AI_BRIDGE_LOCAL_GUIDE.md']
assert data['validations'] == ['smoke_docs', 'release_check', 'diff_check']
assert data['next_safe_command'] == 'git status -sb'
print('OK handoff_template_smoke')

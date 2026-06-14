import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
builder = (ROOT / 'scripts' / 'watcher' / 'command_builder.py').read_text(encoding='utf-8')
assert 'AI_BRIDGE_LOCAL_GOVERNANCE_PREFLIGHT_INTEGRATION_074' in builder
assert 'def governance_preflight_for_command' in builder
assert 'governance_preflight.py' in builder
cmd = [sys.executable, str(ROOT / 'scripts' / 'watcher' / 'governance_preflight.py')]
read = subprocess.run(cmd + ['--command', 'git status -sb'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
mut = subprocess.run(cmd + ['--command', 'git commit -m test'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
read_item = json.loads(read.stdout)
mut_item = json.loads(mut.stdout)
assert read_item['schema'] == 'ai_bridge_local.governance_preflight'
assert read_item['risk_level'] == 'read_only_or_dry_run'
assert read_item['executes_commands'] is False
assert mut_item['risk_level'] == 'mutating'
assert mut_item['requires_manual_review'] is True
assert mut_item['blocks_execution'] is False
print('OK command_builder_governance_smoke')

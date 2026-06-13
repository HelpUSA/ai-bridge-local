import json
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
builder = ROOT / 'scripts' / 'watcher' / 'command_builder.py'
validator = ROOT / 'scripts' / 'watcher' / 'envelope_validator.py'
assert builder.exists(), builder
assert validator.exists(), validator
source = builder.read_text(encoding='utf-8', errors='replace')
for marker in ['command_id', 'source_chat_id', 'target_chat_id', 'delivery_kind']:
 assert marker in source, marker
help_proc = subprocess.run([sys.executable, str(builder), '--help'], cwd=ROOT, text=True, encoding='utf-8', errors='replace', capture_output=True, timeout=30)
assert help_proc.returncode == 0, help_proc.stdout + help_proc.stderr
build_proc = subprocess.run([
 sys.executable, str(builder),
 '--source', '6a2bf3a5-db50-83e9-8f12-2ff1f813cd0b',
 '--target', 'gateway-brain-supervisor',
 '--action', 'run-command',
 '--id', 'smoke_builder_validator_flow',
 '--cwd', 'D:/dev/autocode/ai-bridge-local',
 '--timeout', '30',
 '--command', 'git', 'status', '-sb',
], cwd=ROOT, text=True, encoding='utf-8', errors='replace', capture_output=True, timeout=30)
assert build_proc.returncode == 0, build_proc.stdout + build_proc.stderr
envelope_text = build_proc.stdout
assert '@@AI_BRIDGE_LOCAL_START@@' in envelope_text
assert '@@AI_BRIDGE_LOCAL_END@@' in envelope_text
json_body = ''.join(line for line in envelope_text.splitlines() if not line.startswith('@@'))
env = json.loads(json_body)
assert env['command_id'] == 'smoke_builder_validator_flow'
assert env['delivery_kind'] == 'local_capability'
assert env['target_chat_id'] == 'gateway-brain-supervisor'
assert env['payload']['command'] == ['git', 'status', '-sb']
validate_proc = subprocess.run([sys.executable, str(validator)], input=envelope_text, cwd=ROOT, text=True, encoding='utf-8', errors='replace', capture_output=True, timeout=30)
assert validate_proc.returncode == 0, validate_proc.stdout + validate_proc.stderr
assert 'VALID' in validate_proc.stdout, validate_proc.stdout + validate_proc.stderr
print('OK command_builder_validator_flow_smoke')

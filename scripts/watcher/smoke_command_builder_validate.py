import json, subprocess, sys
from pathlib import Path
ROOT = Path.cwd()
builder = ROOT / 'scripts' / 'watcher' / 'command_builder.py'
validator = ROOT / 'scripts' / 'watcher' / 'envelope_validator.py'
source = builder.read_text(encoding='utf-8', errors='replace')
assert 'command_id' in source
assert 'source_chat_id' in source
assert 'target_chat_id' in source
assert 'delivery_kind' in source
proc = subprocess.run([sys.executable, str(builder), '--help'], cwd=ROOT, text=True, encoding='utf-8', errors='replace', capture_output=True, timeout=30)
assert proc.returncode == 0, proc.stdout + proc.stderr
help_text = proc.stdout + proc.stderr
assert 'command' in help_text.lower(), help_text
assert validator.exists(), validator
print('OK command_builder_validate_smoke')

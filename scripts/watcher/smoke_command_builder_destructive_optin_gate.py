import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
base = [
 sys.executable,
 str(ROOT / 'scripts' / 'watcher' / 'command_builder_destructive_optin_gate.py'),
 '--source',
 'src-chat',
 '--target',
 'gateway-brain-supervisor',
 '--action',
 'run-command',
 '--id',
 'destructive-optin-smoke',
 '--cwd',
 '.',
 '--timeout',
 '60',
]
out = Path(tempfile.mkdtemp()) / 'blocked.txt'
blocked = subprocess.run(base + ['--output-file', str(out), '--command', 'Remove-Item', 'temp', '-Recurse', '-Force'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert blocked.returncode == 40, blocked.stderr + blocked.stdout
allowed_out = Path(tempfile.mkdtemp()) / 'allowed.txt'
allowed = subprocess.run(base + ['--allow-destructive', '--output-file', str(allowed_out), '--command', 'Remove-Item', 'temp', '-Recurse', '-Force'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert allowed.returncode == 0, allowed.stderr + allowed.stdout
assert allowed_out.exists()
print('OK command_builder_destructive_optin_gate_smoke')

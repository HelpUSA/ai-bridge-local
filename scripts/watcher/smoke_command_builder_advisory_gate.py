import subprocess
import sys
import tempfile
from pathlib import Path
ROOT = Path.cwd()
base = [sys.executable, str(ROOT / 'scripts' / 'watcher' / 'command_builder_advisory_gate.py'), '--source', 'src-chat', '--target', 'gateway-brain-supervisor', '--action', 'run-command', '--id', 'gate-smoke', '--cwd', '.', '--timeout', '60']
out = Path(tempfile.mkdtemp()) / 'gate.txt'
ok = subprocess.run(base + ['--output-file', str(out), '--command', 'Remove-Item', 'temp', '-Recurse', '-Force'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert ok.returncode == 0, ok.stderr + ok.stdout
blocked = subprocess.run(base + ['--fail-on-destructive', '--output-file', str(out), '--command', 'Remove-Item', 'temp', '-Recurse', '-Force'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert blocked.returncode == 40, blocked.stderr + blocked.stdout
blocked2 = subprocess.run(base + ['--fail-on-mutating', '--output-file', str(out), '--command', 'git', 'commit', '-m', 'x'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert blocked2.returncode == 40, blocked2.stderr + blocked2.stdout
print('OK command_builder_advisory_gate_smoke')

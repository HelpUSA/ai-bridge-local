import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd().resolve()
args = sys.argv[1:]
allow = '--allow-destructive' in args
args = [x for x in args if x != '--allow-destructive']
gate_args = args if allow else ['--fail-on-destructive'] + args
target = ROOT / 'scripts' / 'watcher' / 'command_builder_advisory_gate.py'
result = subprocess.run([sys.executable, str(target)] + gate_args, cwd=ROOT)
raise SystemExit(result.returncode)

import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd().resolve()
target = ROOT / 'scripts' / 'watcher' / 'command_builder_advisory.py'
result = subprocess.run([sys.executable, str(target)] + sys.argv[1:], cwd=ROOT)
raise SystemExit(result.returncode)

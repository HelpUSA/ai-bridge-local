import subprocess, sys
from pathlib import Path
ROOT = Path.cwd()
script = ROOT / 'scripts' / 'watcher' / 'cleanup_plan.py'
text = script.read_text(encoding='utf-8').lower()
for bad in ['delete ', 'drop ', 'update ']:
 assert bad not in text, bad
proc = subprocess.run([sys.executable, str(script)], cwd=ROOT, text=True, encoding='utf-8', errors='replace', capture_output=True, timeout=30)
out = proc.stdout + proc.stderr
assert proc.returncode == 0, out
assert 'AI_BRIDGE_LOCAL_CLEANUP_PLAN' in out
assert 'No cleanup was executed' in out
print('OK cleanup_plan_smoke')

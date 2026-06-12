import subprocess, sys
from pathlib import Path
ROOT = Path.cwd()
script = ROOT / 'scripts' / 'watcher' / 'post_failure_triage.py'
proc = subprocess.run([sys.executable, str(script), '--limit', '3', '--prefix', 'ai_bridge_local'], cwd=ROOT, text=True, encoding='utf-8', errors='replace', capture_output=True, timeout=30)
out = proc.stdout + proc.stderr
assert proc.returncode == 0, out
assert 'AI_BRIDGE_LOCAL_POST_FAILURE_TRIAGE' in out
assert 'suggestion' in out or 'no matching failures' in out
print('OK post_failure_triage_smoke')

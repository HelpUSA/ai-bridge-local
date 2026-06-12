import subprocess, sys
from pathlib import Path
ROOT = Path.cwd()
cmd = [sys.executable, str(ROOT / 'scripts' / 'watcher' / 'dead_letters_report.py'), '--limit', '3', '--prefix', 'ai_bridge_local']
proc = subprocess.run(cmd, cwd=ROOT, text=True, encoding='utf-8', errors='replace', capture_output=True, timeout=30)
out = proc.stdout + proc.stderr
assert proc.returncode == 0, out
for needle in ['AI_BRIDGE_LOCAL_DEAD_LETTERS_REPORT', 'by_error_kind', 'by_project', 'recent_local_only']:
 assert needle in out, needle
print('OK dead_letters_report_smoke')

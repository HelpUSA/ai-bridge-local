import ast, subprocess, sys
from pathlib import Path
ROOT = Path.cwd()
script = ROOT / 'scripts' / 'watcher' / 'cleanup_plan.py'
text = script.read_text(encoding='utf-8').lower()
for bad in ['delete ', 'drop ', 'update ']:
	assert bad not in text, bad
proc = subprocess.run([sys.executable, str(script), '--min-age-minutes', '30', '--limit', '5'], cwd=ROOT, text=True, encoding='utf-8', errors='replace', capture_output=True, timeout=30)
out = proc.stdout + proc.stderr
assert proc.returncode == 0, out
assert 'AI_BRIDGE_LOCAL_CLEANUP_PLAN' in out
assert 'stale_candidate' in out
assert 'No cleanup was executed' in out
for line in out.splitlines():
	if 'age_minutes' in line and line.strip().startswith('{'):
		data = ast.literal_eval(line.strip())
		assert data.get('age_minutes', 0) >= 0, line
print('OK cleanup_plan_smoke')

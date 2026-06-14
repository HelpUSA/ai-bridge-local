import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
tracked_rel = 'scripts/watcher/_rollback_helper_smoke_tracked.txt'
untracked_rel = 'scripts/watcher/_rollback_helper_smoke_untracked.txt'
tracked = ROOT / tracked_rel
untracked = ROOT / untracked_rel
tracked.unlink(missing_ok=True)
untracked.unlink(missing_ok=True)
tracked.write_text('base' + chr(10), encoding='utf-8', newline=chr(10))
subprocess.run(['git', 'add', tracked_rel], cwd=ROOT, check=True)
tracked.write_text('changed' + chr(10), encoding='utf-8', newline=chr(10))
untracked.write_text('temp' + chr(10), encoding='utf-8', newline=chr(10))
cp = subprocess.run([sys.executable, str(ROOT / 'scripts/watcher/rollback_helper.py'), '--cwd', '.'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert cp.returncode == 0, cp.stdout + cp.stderr
data = json.loads(cp.stdout)
assert data['status'] == 'plan', data
assert any(x['path'] == tracked_rel for x in data['restore_candidates']), data
assert any(x['path'] == untracked_rel for x in data['untracked_candidates']), data
cp = subprocess.run([sys.executable, str(ROOT / 'scripts/watcher/rollback_helper.py'), '--cwd', '.', '--restore', '--path', tracked_rel], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert cp.returncode == 0, cp.stdout + cp.stderr
assert tracked.read_text(encoding='utf-8') == 'base' + chr(10)
cp = subprocess.run([sys.executable, str(ROOT / 'scripts/watcher/rollback_helper.py'), '--cwd', '.', '--delete-untracked', '--path', untracked_rel], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert cp.returncode == 0, cp.stdout + cp.stderr
data = json.loads(cp.stdout)
assert data['actions'][0]['action'] == 'refuse_untracked_without_explicit_confirmation', data
assert untracked.exists()
cp = subprocess.run([sys.executable, str(ROOT / 'scripts/watcher/rollback_helper.py'), '--cwd', '.', '--delete-untracked', '--confirm-delete-untracked', untracked_rel, '--path', untracked_rel], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert cp.returncode == 0, cp.stdout + cp.stderr
assert not untracked.exists()
subprocess.run(['git', 'restore', '--staged', '--', tracked_rel], cwd=ROOT, check=True)
tracked.unlink(missing_ok=True)
print('OK rollback_helper_smoke')

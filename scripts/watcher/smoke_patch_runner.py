import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd()
target = ROOT / 'temp' / 'patch_runner_smoke_target.txt'
patch = ROOT / 'temp' / 'patch_runner_smoke.patch'
target.unlink(missing_ok=True)
patch.parent.mkdir(exist_ok=True)
lf = chr(10)
patch_lines = ['diff --git a/temp/patch_runner_smoke_target.txt b/temp/patch_runner_smoke_target.txt', 'new file mode 100644', 'index 0000000..d95f3ad', '--- /dev/null', '+++ b/temp/patch_runner_smoke_target.txt', '@@ -0,0 +1 @@', '+patch runner smoke']
patch.write_text(lf.join(patch_lines) + lf, encoding='utf-8', newline=lf)
cp = subprocess.run([sys.executable, str(ROOT / 'scripts/watcher/patch_runner.py'), '--patch-file', 'temp/patch_runner_smoke.patch', '--cwd', '.'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert cp.returncode == 0, cp.stdout + cp.stderr
data = json.loads(cp.stdout)
assert data['status'] == 'checked', data
assert not target.exists()
cp = subprocess.run([sys.executable, str(ROOT / 'scripts/watcher/patch_runner.py'), '--patch-file', 'temp/patch_runner_smoke.patch', '--cwd', '.', '--apply'], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert cp.returncode == 0, cp.stdout + cp.stderr
data = json.loads(cp.stdout)
assert data['status'] == 'applied', data
assert target.read_text(encoding='utf-8') == 'patch runner smoke' + lf
target.unlink()
patch.unlink()
print('OK patch_runner_smoke')

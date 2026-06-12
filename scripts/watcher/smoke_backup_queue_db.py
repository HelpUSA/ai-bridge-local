import subprocess, sys
from pathlib import Path
ROOT = Path.cwd()
backup_dir = ROOT / 'backups' / 'queue_local'
proc = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'backup_queue_db.py')], cwd=ROOT, text=True, encoding='utf-8', errors='replace', capture_output=True, timeout=60)
out = proc.stdout + proc.stderr
assert proc.returncode == 0, out
files = sorted(backup_dir.glob('queue_local_*.db')) if backup_dir.exists() else []
assert files, 'backup file was not created'
latest = max(files, key=lambda p: p.stat().st_mtime)
assert latest.stat().st_size > 0, str(latest)
status = subprocess.run(['git', 'status', '--porcelain', '--', 'backups/queue_local'], cwd=ROOT, text=True, encoding='utf-8', errors='replace', capture_output=True, timeout=30).stdout.strip()
assert status == '', status
print('OK backup_queue_db_smoke')

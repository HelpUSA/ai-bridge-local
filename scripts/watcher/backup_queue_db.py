import shutil, time
from pathlib import Path
ROOT = Path.cwd()
DB = ROOT / 'queue_local.db'
BACKUP_DIR = ROOT / 'backups' / 'queue_local'
BACKUP_DIR.mkdir(parents=True, exist_ok=True)
stamp = time.strftime('%Y%m%d_%H%M%S')
dst = BACKUP_DIR / ('queue_local_' + stamp + '.db')
if not DB.exists(): raise SystemExit('queue_local.db not found')
shutil.copy2(DB, dst)
print('OK queue_db_backup', dst)

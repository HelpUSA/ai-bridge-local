from pathlib import Path
ROOT = Path.cwd()
script = ROOT / 'scripts' / 'watcher' / 'backup_queue_db.py'
assert script.exists(), script
text = script.read_text(encoding='utf-8')
assert 'queue_local.db' in text
assert 'backups' in text
assert 'shutil.copy2' in text
print('OK backup_queue_db_smoke')

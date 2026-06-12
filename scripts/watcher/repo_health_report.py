import json, sqlite3, subprocess
from pathlib import Path
ROOT = Path.cwd()
print('AI_BRIDGE_LOCAL_REPO_HEALTH')
p = subprocess.run(['git', 'status', '-sb'], cwd=ROOT, text=True, encoding='utf-8', errors='replace', capture_output=True)
print('git_status', p.returncode, (p.stdout or '').strip())
p = subprocess.run(['git', 'log', '--oneline', '-1'], cwd=ROOT, text=True, encoding='utf-8', errors='replace', capture_output=True)
print('git_head', p.returncode, (p.stdout or '').strip())
manifest = ROOT / 'extension' / 'manifest.json'
data = json.loads(manifest.read_text(encoding='utf-8-sig')) if manifest.exists() else {}
print('manifest_version', data.get('version', ''))
db = ROOT / 'queue_local.db'
print('db_exists', db.exists(), 'db_size', db.stat().st_size if db.exists() else 0)
rows = []
if db.exists(): rows = list(sqlite3.connect(db).execute('select status,count(1) from commands group by status order by status'))
for status, n in rows: print('status_count', status, n)
print('AI_BRIDGE_LOCAL_REPO_HEALTH_DONE')

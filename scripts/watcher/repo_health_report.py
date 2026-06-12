import json, sqlite3, subprocess
from pathlib import Path
ROOT = Path.cwd()
def run(cmd): p = subprocess.run(cmd, cwd=ROOT, text=True, encoding='utf-8', errors='replace', capture_output=True); return p.returncode, (p.stdout or '').strip()
print('AI_BRIDGE_LOCAL_REPO_HEALTH')
rc, out = run(['git', 'status', '-sb'])
print('git_status', rc, out)
rc, out = run(['git', 'log', '--oneline', '-1'])
print('git_head', rc, out)
manifest = ROOT / 'extension' / 'manifest.json'
data = json.loads(manifest.read_text(encoding='utf-8-sig')) if manifest.exists() else {}
print('manifest_version', data.get('version', ''))
db = ROOT / 'queue_local.db'
size = db.stat().st_size if db.exists() else 0
print('db_exists', db.exists(), 'db_size_mb', round(size / 1048576, 2))
con = sqlite3.connect(db) if db.exists() else None
if con: con.row_factory = sqlite3.Row
rows = list(con.execute('select status,count(1) from commands group by status order by status')) if con else []
for status, n in rows: print('status_count', status, n)
for name in ['invalid_messages', 'dead_letters']: print('table_count', name, con.execute('select count(1) from ' + name).fetchone()[0] if con else 0)
row = con.execute('select command_id,created_at from commands where status=? order by created_at asc limit 1', ('delivering',)).fetchone() if con else None
print('oldest_delivering', row['command_id'] if row else '', row['created_at'] if row else '')
if con: con.close()
print('AI_BRIDGE_LOCAL_REPO_HEALTH_DONE')

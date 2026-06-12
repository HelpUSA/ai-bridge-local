import json, sqlite3, subprocess
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path.cwd()
def run(cmd): p = subprocess.run(cmd, cwd=ROOT, text=True, encoding='utf-8', errors='replace', capture_output=True); return p.returncode, (p.stdout or '').strip()
def age_minutes(value):
	if not value: return None
	dt = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
	if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
	return max(0, int((datetime.now(timezone.utc) - dt.astimezone(timezone.utc)).total_seconds() // 60))
print('AI_BRIDGE_LOCAL_REPO_HEALTH')
alerts = []
rc, out = run(['git', 'status', '-sb'])
print('git_status', rc, out)
if rc != 0: alerts.append('git_status_failed')
rc, out = run(['git', 'log', '--oneline', '-1'])
print('git_head', rc, out)
manifest = ROOT / 'extension' / 'manifest.json'
data = json.loads(manifest.read_text(encoding='utf-8-sig')) if manifest.exists() else {}
print('manifest_version', data.get('version', ''))
db = ROOT / 'queue_local.db'
size = db.stat().st_size if db.exists() else 0
print('db_exists', db.exists(), 'db_size_mb', round(size / 1048576, 2))
con = sqlite3.connect(db) if db.exists() else None
status_map = {}
oldest_age = None
if con:
	con.row_factory = sqlite3.Row
	rows = list(con.execute('select status,count(1) from commands group by status order by status'))
	for status, n in rows: status_map[status] = n; print('status_count', status, n)
	for name in ['invalid_messages', 'dead_letters']: print('table_count', name, con.execute('select count(1) from ' + name).fetchone()[0])
	row = con.execute('select command_id,created_at from commands where status=? order by created_at asc limit 1', ('delivering',)).fetchone()
	oldest_age = age_minutes(row['created_at']) if row else None
	print('oldest_delivering', row['command_id'] if row else '', row['created_at'] if row else '', 'age_minutes', oldest_age if oldest_age is not None else '')
	con.close()
if status_map.get('queued', 0) > 0: alerts.append('queued_commands_present')
if oldest_age is not None and oldest_age > 30: alerts.append('old_delivering_present')
print('health_status', 'WARN' if alerts else 'OK')
for alert in alerts: print('health_alert', alert)
print('AI_BRIDGE_LOCAL_REPO_HEALTH_DONE')

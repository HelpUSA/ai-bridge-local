import sqlite3
from pathlib import Path
ROOT = Path.cwd()
DB = ROOT / 'queue_local.db'
print('AI_BRIDGE_LOCAL_CLEANUP_PLAN')
if not DB.exists(): raise SystemExit('queue_local.db not found')
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
print('delivering_candidates_report_only')
try:
 rows = list(con.execute('select id,command_id,target_chat_id,status,created_at from commands where status=? order by id asc limit 20', ('delivering',)))
 for row in rows: print(str(dict(row)).encode('ascii', 'backslashreplace').decode('ascii'))
except Exception as exc: print('delivering_query_error', str(exc))
print('failed_recent_report_only')
try:
 rows = list(con.execute('select id,command_id,target_chat_id,status,created_at from commands where status=? order by id desc limit 20', ('failed',)))
 for row in rows: print(str(dict(row)).encode('ascii', 'backslashreplace').decode('ascii'))
except Exception as exc: print('failed_query_error', str(exc))
con.close()
print('No cleanup was executed. Run backup_queue_db.py before any future cleanup.')

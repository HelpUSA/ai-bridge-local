import argparse, sqlite3
from datetime import datetime
from pathlib import Path
ROOT = Path.cwd()
DB = ROOT / 'queue_local.db'
parser = argparse.ArgumentParser()
parser.add_argument('--min-age-minutes', type=int, default=30)
parser.add_argument('--limit', type=int, default=20)
args = parser.parse_args()
def safe(obj): print(str(obj).encode('ascii', 'backslashreplace').decode('ascii'))
def age_minutes(value): return int((datetime.now() - datetime.fromisoformat(str(value).replace('Z', ''))).total_seconds() // 60) if value else None
print('AI_BRIDGE_LOCAL_CLEANUP_PLAN')
print('mode', 'report_only')
print('min_age_minutes', args.min_age_minutes)
if not DB.exists(): raise SystemExit('queue_local.db not found')
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
print('delivering_candidates_report_only')
for row in con.execute('select id,command_id,target_chat_id,status,created_at from commands where status=? order by id asc limit ?', ('delivering', args.limit)): d=dict(row); a=age_minutes(d.get('created_at')); d['age_minutes']=a; d['stale_candidate']=bool(a is not None and a >= args.min_age_minutes); safe(d)
print('failed_recent_report_only')
for row in con.execute('select id,command_id,target_chat_id,status,created_at from commands where status=? order by id desc limit ?', ('failed', args.limit)): safe(dict(row))
con.close()
print('No cleanup was executed. Run backup_queue_db.py before any future cleanup.')

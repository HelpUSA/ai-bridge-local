import json
import sqlite3
from pathlib import Path
ROOT = Path.cwd()
candidates = [ROOT / 'runtime' / 'gateway_queue.sqlite3', ROOT / 'queue.sqlite3', ROOT / 'gateway_queue.sqlite3']
db = next((item for item in candidates if item.exists()), None)
payload = {'schema': 'ai_bridge_local.dead_letters_review', 'executes_commands': False, 'db_found': bool(db), 'db_path': str(db) if db else '', 'recommendation': 'read-only review first; cleanup only after explicit approval'}
rows = []
conn = sqlite3.connect(str(db)) if db else None
cur = conn.cursor() if conn else None
rows = cur.execute('select name from sqlite_master where type = ''table'' order by name').fetchall() if cur else []
payload['tables'] = [item[0] for item in rows]
conn.close() if conn else None
print(json.dumps(payload, ensure_ascii=False, indent=2))

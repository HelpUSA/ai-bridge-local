import ast
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path.cwd()
script = ROOT / 'scripts' / 'watcher' / 'cleanup_plan.py'
text = script.read_text(encoding='utf-8').lower()
for bad in ['delete ', 'drop ', 'update ']:
 assert bad not in text, bad

with tempfile.TemporaryDirectory(prefix='ai_bridge_cleanup_smoke_') as tmp:
 tmp_root = Path(tmp)
 tmp_script_dir = tmp_root / 'scripts' / 'watcher'
 tmp_script_dir.mkdir(parents=True)
 shutil.copy2(script, tmp_script_dir / 'cleanup_plan.py')

 db = tmp_root / 'queue_local.db'
 con = sqlite3.connect(db)
 con.execute(
 'create table commands (id integer primary key, command_id text, target_chat_id text, status text, created_at text)'
 )
 old = (datetime.now(timezone.utc) - timedelta(minutes=90)).isoformat()
 recent = datetime.now(timezone.utc).isoformat()
 con.execute(
 'insert into commands (command_id,target_chat_id,status,created_at) values (?,?,?,?)',
 ('smoke-old-delivering', 'gateway-brain-supervisor', 'delivering', old),
 )
 con.execute(
 'insert into commands (command_id,target_chat_id,status,created_at) values (?,?,?,?)',
 ('smoke-recent-failed', 'gateway-brain-supervisor', 'failed', recent),
 )
 con.commit()
 con.close()

 proc = subprocess.run(
 [sys.executable, str(tmp_script_dir / 'cleanup_plan.py'), '--min-age-minutes', '30', '--limit', '5'],
 cwd=tmp_root,
 text=True,
 encoding='utf-8',
 errors='replace',
 capture_output=True,
 timeout=30,
 )

out = proc.stdout + proc.stderr
assert proc.returncode == 0, out
assert 'AI_BRIDGE_LOCAL_CLEANUP_PLAN' in out
assert 'mode report_only' in out
assert 'stale_candidate' in out
assert 'No cleanup was executed' in out
assert 'smoke-old-delivering' in out

saw_stale_candidate = False
for line in out.splitlines():
 if 'age_minutes' in line and line.strip().startswith('{'):
 data = ast.literal_eval(line.strip())
 assert data.get('age_minutes', 0) >= 0, line
 if data.get('command_id') == 'smoke-old-delivering':
 assert data.get('stale_candidate') is True, line
 saw_stale_candidate = True

assert saw_stale_candidate, out
print('OK cleanup_plan_smoke')

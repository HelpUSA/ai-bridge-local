# -- coding: utf-8 --
from pathlib import Path
import json, os, sqlite3, subprocess, sys
from datetime import datetime, timezone

ROOT = Path.cwd()

def section(name):
 print()
 print('## ' + name)

def run(label, cmd):
 try:
 proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=25)
 print(label + ': rc=' + str(proc.returncode))
 if proc.stdout.strip():
 print(proc.stdout.strip())
 if proc.stderr.strip():
 print('STDERR:')
 print(proc.stderr.strip())
 return proc.returncode
 except Exception as exc:
 print(label + ': error=' + repr(exc))
 return 999

def find_db():
 candidates = [ROOT / 'queue_local.db', ROOT / 'runtime' / 'queue_local.db', ROOT / 'data' / 'queue_local.db', ROOT / 'db' / 'queue_local.db']
 for item in candidates:
 if item.exists():
 return item
 hits = sorted(ROOT.glob('**/queue_local.db'))
 return hits[0] if hits else None

def db_section():
 section('database')
 db = find_db()
 if not db:
 print('queue_local.db: not found')
 return
 print('db=' + str(db))
 print('db_size_bytes=' + str(db.stat().st_size))
 with sqlite3.connect(db) as con:
 tables = [r[0] for r in con.execute('select name from sqlite_master where type=''table'' order by name')]
 print('tables=' + ', '.join(tables))
 for table in ['commands', 'invalid_messages', 'dead_letters']:
 if table in tables:
 count = con.execute('select count() from ' + table).fetchone()[0]
 print(table + '_count=' + str(count))
 if 'commands' in tables:
 try:
 rows = con.execute('select status, count() from commands group by status order by status').fetchall()
 print('commands_status_counts:')
 for status, count in rows:
 print('- ' + str(status) + ': ' + str(count))
 except Exception as exc:
 print('commands_status_counts_error=' + repr(exc))

def versions_section():
 section('versions')
 for rel in ['extension/manifest.json', 'extension/content_script.js', 'extension/background.js']:
 f = ROOT / rel
 if not f.exists():
 print(rel + ': missing')
 continue
 text = f.read_text(encoding='utf-8', errors='replace')
 if rel.endswith('.json'):
 try:
 data = json.loads(text.lstrip('﻿'))
 print(rel + ': version=' + str(data.get('version')))
 except Exception as exc:
 print(rel + ': json_error=' + repr(exc))
 else:
 found = [line.strip() for line in text.splitlines() if 'VERSION' in line][:3]
 print(rel + ': ' + (' | '.join(found) if found else 'version marker not found'))

def main():
 print('AI_BRIDGE_LOCAL_HEALTH_CHECK')
 print('root=' + str(ROOT))
 print('time_utc=' + datetime.now(timezone.utc).isoformat())
 section('git')
 run('git status', ['git', 'status', '-sb'])
 run('git log', ['git', 'log', '--oneline', '--decorate', '-5'])
 section('locks')
 lock = ROOT / '.git' / 'index.lock'
 print('.git/index.lock=' + ('present' if lock.exists() else 'absent'))
 section('process hints')
 if os.name == 'nt':
 run('git processes', ['powershell', '-NoProfile', '-Command', 'Get-Process git -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,StartTime,Path | Format-Table -AutoSize | Out-String -Width 4096'])
 run('bridge python processes', ['powershell', '-NoProfile', '-Command', 'Get-CimInstance Win32_Process | Where-Object { $PSItem.Name -match ''python'' -and $PSItem.CommandLine -match ''gateway|worker|control|bridge'' } | Select-Object ProcessId,Name,CommandLine | Format-Table -AutoSize | Out-String -Width 4096'])
 versions_section()
 db_section()
 section('smoke')
 smoke = ROOT / 'scripts' / 'watcher' / 'smoke_robustness.py'
 if smoke.exists():
 run('smoke_robustness', [sys.executable, str(smoke)])
 else:
 print('smoke_robustness.py: missing')
 print()
 print('AI_BRIDGE_LOCAL_HEALTH_CHECK_DONE')
 return 0

if name == 'main':
 raise SystemExit(main())

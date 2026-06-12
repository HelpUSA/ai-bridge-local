import argparse, sqlite3
from pathlib import Path
ROOT = Path.cwd()
DB = ROOT / 'queue_local.db'
parser = argparse.ArgumentParser()
parser.add_argument('--limit', type=int, default=20)
parser.add_argument('--prefix', default='ai_bridge_local')
args = parser.parse_args()
limit = max(1, min(args.limit, 100))
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
def safe(obj): print(str(obj).encode('ascii', 'backslashreplace').decode('ascii'))
def kind(text):
 t = (text or '').lower()
 if 'syntaxerror' in t or 'indentationerror' in t: return 'python_compile'
 if 'json' in t or 'parse' in t: return 'json_parse'
 if 'diff_check' in t: return 'diff_check'
 if 'validate_all' in t: return 'validate_all'
 if 'timeout' in t: return 'timeout'
 if not t.strip(): return 'empty_error'
 return 'other'
print('AI_BRIDGE_LOCAL_DEAD_LETTERS_REPORT')
rows = list(con.execute('select command_id,target_chat_id,last_error,failed_at from dead_letters'))
by_kind = {}
by_project = {}
for r in rows:
 cid = r['command_id'] or ''
 project = cid.split('_')[0] if cid else 'unknown'
 by_project[project] = by_project.get(project, 0) + 1
 k = kind(r['last_error'])
 by_kind[k] = by_kind.get(k, 0) + 1
print('by_error_kind')
for k,n in sorted(by_kind.items(), key=lambda x: x[1], reverse=True)[:limit]: safe({'kind':k,'n':n})
print('by_project')
for k,n in sorted(by_project.items(), key=lambda x: x[1], reverse=True)[:limit]: safe({'project':k,'n':n})
print('recent_local_only')
for r in con.execute('select id,command_id,last_error,failed_at from dead_letters where command_id like ? order by id desc limit ?', (args.prefix + '%', limit)): safe(dict(r))
con.close()

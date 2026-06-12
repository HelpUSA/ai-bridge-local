import argparse, sqlite3
from pathlib import Path
ROOT = Path.cwd()
DB = ROOT / 'queue_local.db'
parser = argparse.ArgumentParser()
parser.add_argument('--limit', type=int, default=20)
parser.add_argument('--prefix', default='ai_bridge_local')
parser.add_argument('--target', default='')
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
def project(command_id):
	cid = command_id or ''
	if cid.startswith('ai_bridge_local'): return 'ai_bridge_local'
	if cid.startswith('pizza'): return 'pizza'
	if cid.startswith('helpus'): return 'helpus'
	if cid.startswith('trading'): return 'trading'
	return cid.split('_')[0] if cid else 'unknown'
where = []
params = []
if args.target: where.append('target_chat_id=?'); params.append(args.target)
sql_where = (' where ' + ' and '.join(where)) if where else ''
print('AI_BRIDGE_LOCAL_DEAD_LETTERS_REPORT')
print('filters', {'prefix': args.prefix, 'target': args.target, 'limit': limit})
rows = list(con.execute('select command_id,target_chat_id,last_error,failed_at from dead_letters' + sql_where, params))
by_kind = {}
by_project = {}
for r in rows:
	by_project[project(r['command_id'])] = by_project.get(project(r['command_id']), 0) + 1
	k = kind(r['last_error'])
	by_kind[k] = by_kind.get(k, 0) + 1
print('by_error_kind')
for k,n in sorted(by_kind.items(), key=lambda x: x[1], reverse=True)[:limit]: safe({'kind':k,'n':n})
print('by_project')
for k,n in sorted(by_project.items(), key=lambda x: x[1], reverse=True)[:limit]: safe({'project':k,'n':n})
print('recent_local_only')
recent_where = ['command_id like ?']
recent_params = [args.prefix + '%']
if args.target: recent_where.append('target_chat_id=?'); recent_params.append(args.target)
recent_params.append(limit)
recent_sql = 'select id,command_id,target_chat_id,last_error,failed_at from dead_letters where ' + ' and '.join(recent_where) + ' order by id desc limit ?'
for r in con.execute(recent_sql, recent_params): safe(dict(r))
con.close()

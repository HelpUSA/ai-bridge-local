import argparse, sqlite3
from pathlib import Path
ROOT = Path.cwd()
DB = ROOT / 'queue_local.db'
parser = argparse.ArgumentParser()
parser.add_argument('--limit', type=int, default=10)
parser.add_argument('--target', default='')
parser.add_argument('--command-prefix', default='')
args = parser.parse_args()
limit = max(1, min(args.limit, 100))
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
def safe(v): return str(dict(v)).encode('ascii', 'backslashreplace').decode('ascii')
def emit(v): print(safe(v))
def where(prefix=False):
 parts = []
 vals = []
 if args.target:
  parts.append('target_chat_id = ?')
  vals.append(args.target)
 if prefix and args.command_prefix:
  parts.append('command_id like ?')
  vals.append(args.command_prefix + '%')
 return ((' where ' + ' and '.join(parts)) if parts else ''), vals
print('AI_BRIDGE_LOCAL_DIAGNOSTICS')
print('repo=', ROOT)
print('filters', {'limit': limit, 'target': args.target, 'command_prefix': args.command_prefix})
print('status_counts')
for r in con.execute('select status,count(1) n from commands group by status order by status'): emit(r)
print('invalid_messages_recent')
for r in con.execute('select id,source_chat_id,error,created_at from invalid_messages order by id desc limit ?', (limit,)): emit(r)
print('dead_letters_recent')
w, vals = where(True)
for r in con.execute('select id,command_id,target_chat_id,last_error,failed_at from dead_letters' + w + ' order by id desc limit ?', vals + [limit]): emit(r)
print('failed_commands_recent')
w, vals = where(True)
if w: w = w + ' and status = ?'
else: w = ' where status = ?'
vals = vals + ['failed', limit]
for r in con.execute('select id,command_id,target_chat_id,last_error,created_at from commands' + w + ' order by id desc limit ?', vals): emit(r)
print('dead_letters_by_target')
for r in con.execute('select target_chat_id,count(1) n from dead_letters group by target_chat_id order by n desc limit ?', (limit,)): emit(r)
con.close()
# usage: python scripts/watcher/control_center_diagnostics.py --limit 20 --target gateway-brain-supervisor --command-prefix ai_bridge_local

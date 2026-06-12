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
def emit_obj(obj): print(str(obj).encode('ascii', 'backslashreplace').decode('ascii'))
def emit(row): emit_obj(dict(row))
print('AI_BRIDGE_LOCAL_DEAD_LETTERS_REPORT')
print('by_target')
for r in con.execute('select target_chat_id,count(1) n from dead_letters group by target_chat_id order by n desc limit ?', (limit,)): emit(r)
print('by_command_family')
families = {}
for r in con.execute('select command_id from dead_letters'):
 cid = r['command_id'] or ''
 family = cid.split('_')[0] if cid else 'unknown'
 families[family] = families.get(family, 0) + 1
for family, n in sorted(families.items(), key=lambda item: item[1], reverse=True)[:limit]:
 emit_obj({'family': family, 'n': n})
print('recent_local_only')
for r in con.execute('select id,command_id,last_error,failed_at from dead_letters where command_id like ? order by id desc limit ?', (args.prefix + '%', limit)): emit(r)
con.close()

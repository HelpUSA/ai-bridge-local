import argparse, sqlite3
from pathlib import Path
ROOT = Path.cwd()
DB = ROOT / 'queue_local.db'
parser = argparse.ArgumentParser()
parser.add_argument('--limit', type=int, default=5)
parser.add_argument('--prefix', default='ai_bridge_local')
args = parser.parse_args()
def safe(obj): print(str(obj).encode('ascii', 'backslashreplace').decode('ascii'))
def category(text):
	t = (text or '').lower()
	if 'syntaxerror' in t or 'indentationerror' in t: return 'python_compile'
	if 'json' in t or 'parse' in t: return 'json_parse'
	if 'diff_check' in t: return 'diff_check'
	if 'validate_all' in t: return 'validation'
	if 'timeout' in t: return 'timeout'
	return 'other'
def suggestion(cat):
	if cat == 'python_compile': return 'restore or patch only the broken file, then run py_compile before commit'
	if cat == 'json_parse': return 'resend smaller envelope or use script_ext/script_text; avoid large inline JSON'
	if cat == 'diff_check': return 'trim trailing blanks, run git diff --check, then validate_all'
	if cat == 'validation': return 'run the failing smoke alone, fix only that scope, then release_check'
	if cat == 'timeout': return 'split command into smaller steps and inspect partial state first'
	return 'inspect last_error, git status, and retry with a smaller safe command'
print('AI_BRIDGE_LOCAL_POST_FAILURE_TRIAGE')
if not DB.exists(): raise SystemExit('queue_local.db not found')
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
rows = list(con.execute('select id,command_id,target_chat_id,last_error,failed_at from dead_letters where command_id like ? order by id desc limit ?', (args.prefix + '%', args.limit)))
if not rows: print('no matching failures')
for row in rows:
	d = dict(row)
	cat = category(d.get('last_error'))
	d['category'] = cat
	d['suggestion'] = suggestion(cat)
	err = d.get('last_error') or ''
	d['last_error'] = err[:500]
	safe(d)
con.close()

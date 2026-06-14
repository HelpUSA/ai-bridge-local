import json
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TMP = ROOT / 'temp'
TMP.mkdir(exist_ok=True)
DB = TMP / 'inspect_delivery_failure_smoke.db'
if DB.exists():
	DB.unlink()
con = sqlite3.connect(DB)
con.execute('create table commands (id integer primary key, command_id text, source_chat_id text, target_chat_id text, action text, delivery_kind text, conversation_id text, from_agent text, message text, payload_json text, status text, created_at text, delivered_at text, acked_at text, return_code integer, stdout text, stderr text, last_error text)')
con.execute('create table dead_letters (id integer primary key, command_id text, source_chat_id text, target_chat_id text, action text, delivery_kind text, payload_json text, last_error text, attempt_count integer, failed_at text)')
con.execute('create table events (id integer primary key, command_id text, event_type text, message text, payload_json text, created_at text)')
con.execute('create table invalid_messages (id integer primary key, source_chat_id text, raw_text text, error text, created_at text)')
con.execute('insert into commands (command_id,status,last_error,stderr) values (?,?,?,?)', ('cmd-submit', 'failed', 'submit_button_not_found_or_disabled', ''))
con.execute('insert into dead_letters (command_id,last_error,attempt_count) values (?,?,?)', ('cmd-parse', 'envelope_parse_error bad JSON', 1))
con.execute('insert into invalid_messages (source_chat_id,raw_text,error) values (?,?,?)', ('smoke', 'cmd-parse raw', 'bad_delivery_kind'))
con.commit()

def run(*args):
	cp = subprocess.run([sys.executable, str(ROOT / 'scripts/watcher/inspect_delivery_failure.py'), '--db', str(DB), *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if cp.returncode != 0:
		raise AssertionError(cp.stderr)
	return json.loads(cp.stdout)

one = run('--command-id', 'cmd-submit')
assert one['schema'] == 'ai_bridge_local.inspect_delivery_failure', one
assert one['status'] == 'found', one
assert one['diagnosis']['category'] == 'submit_button_not_found_or_disabled', one
two = run('--command-id', 'cmd-parse')
assert two['summary']['dead_letters'] == 1, two
assert two['diagnosis']['category'] == 'envelope_parse_error', two
recent = run('--limit', '2')
assert recent['summary']['commands'] >= 1, recent
missing = run('--command-id', 'missing-command')
assert missing['status'] == 'not_found', missing
print('OK inspect_delivery_failure_smoke')

import sqlite3
from pathlib import Path
ROOT=Path.cwd()
DB=ROOT/'queue_local.db'
con=sqlite3.connect(DB)
con.row_factory=sqlite3.Row
emit=lambda v: print(str(dict(v)).encode('ascii','backslashreplace').decode('ascii'))
print('AI_BRIDGE_LOCAL_DIAGNOSTICS')
print('repo=',ROOT)
print('status_counts')
[emit(r) for r in con.execute('select status,count(1) n from commands group by status order by status')]
print('invalid_messages_recent')
[emit(r) for r in con.execute('select id,source_chat_id,error,created_at from invalid_messages order by id desc limit 10')]
print('dead_letters_recent')
[emit(r) for r in con.execute('select id,command_id,target_chat_id,last_error,failed_at from dead_letters order by id desc limit 10')]
print('failed_commands_recent')
[emit(r) for r in con.execute('select id,command_id,target_chat_id,last_error,created_at from commands where status=? order by id desc limit 10', ('failed',))]
con.close()

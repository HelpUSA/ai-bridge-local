import sqlite3, json
from pathlib import Path
ROOT=Path(file).resolve().parents[2]
DB=ROOT/'queue_local.db'
def rows(sql,args=()):
 con=sqlite3.connect(DB); con.row_factory=sqlite3.Row
 try: return [dict(r) for r in con.execute(sql,args)]
 finally: con.close()
def main():
 print('AI_BRIDGE_LOCAL_DIAGNOSTICS')
 print('repo=',ROOT)
 print('status_counts')
 for r in rows('select status,count(1) n from commands group by status order by status'): print(r)
 print('invalid_messages_recent')
 for r in rows('select id,source_chat_id,error,created_at from invalid_messages order by id desc limit 10'): print(r)
 print('dead_letters_recent')
 for r in rows('select id,command_id,target_chat_id,last_error,failed_at from dead_letters order by id desc limit 10'): print(r)
 print('failed_commands_recent')
 for r in rows('select id,command_id,target_chat_id,last_error,created_at from commands where status=''failed'' order by id desc limit 10'): print(r)
if name=='main': main()


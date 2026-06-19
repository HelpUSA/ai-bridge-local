import sqlite3

conn = sqlite3.connect("queue_local.db")

print("result_to status counts:")
for row in conn.execute("select status, count(*) from commands where command_id like 'result_to_%' group by status order by status").fetchall():
    print(row)

print("local_status_accepted_result_to status counts:")
for row in conn.execute("select status, count(*) from commands where command_id like 'local_status_accepted_result_to_%' group by status order by status").fetchall():
    print(row)

print("recent result rows:")
for row in conn.execute("""
select id, command_id, action, status, source_chat_id, target_chat_id
from commands
where command_id like 'result_to_%'
   or command_id like 'local_status_accepted_result_to_%'
order by id desc
limit 50
""").fetchall():
    print(row)

conn.close()

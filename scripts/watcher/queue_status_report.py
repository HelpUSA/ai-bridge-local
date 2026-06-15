import argparse, sqlite3
parser=argparse.ArgumentParser()
parser.add_argument('--limit', type=int, default=20)
parser.add_argument('--status', default='')
args=parser.parse_args()
conn=sqlite3.connect('queue_local.db')
print('QUEUE_STATUS_REPORT_START')
print('status_counts', conn.execute('select status, count(*) from commands group by status order by status').fetchall())
sql='select command_id, source_chat_id, target_chat_id, action, status, created_at, delivered_at, acked_at, last_error from commands'
sql=sql+(' where status=?' if args.status else '')+' order by id desc limit ?'
params=([args.status] if args.status else [])+[args.limit]
print('items', conn.execute(sql, tuple(params)).fetchall())
conn.close()
print('QUEUE_STATUS_REPORT_END')

#!/usr/bin/env python3
import argparse
import sqlite3

DB_PATH = 'queue_local.db'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prefix', default='ai_bridge_local_')
    parser.add_argument('--conversation', default='')
    parser.add_argument('--source-chat-id', default='')
    parser.add_argument('--limit', type=int, default=50)
    args = parser.parse_args()

    where = []
    params = []
    title_parts = []

    if args.prefix:
        where.append('command_id like ?')
        params.append(args.prefix + '%')
        title_parts.append('prefix=' + args.prefix)

    if args.conversation:
        where.append('conversation_id = ?')
        params.append(args.conversation)
        title_parts.append('conversation=' + args.conversation)

    if args.source_chat_id:
        where.append('source_chat_id = ?')
        params.append(args.source_chat_id)
        title_parts.append('source_chat_id=' + args.source_chat_id)

    clause = ''
    if where:
        clause = ' where ' + ' and '.join(where)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    print('AI_BRIDGE_LOCAL_FILTERED_DB_STATUS_START')
    print('FILTER|' + ('|'.join(title_parts) if title_parts else 'none'))

    print('STATUS_COUNTS')
    for row in cur.execute('select status,count(*) from commands' + clause + ' group by status order by status', params).fetchall():
        print(str(row[0]) + '|' + str(row[1]))

    print('RECENT_COMMANDS')
    sql = 'select id,command_id,action,status,return_code,conversation_id,created_at from commands' + clause + ' order by id desc limit ?'
    for row in cur.execute(sql, params + [args.limit]).fetchall():
        print('|'.join('' if x is None else str(x)[:180] for x in row))

    con.close()
    print('AI_BRIDGE_LOCAL_FILTERED_DB_STATUS_END')

if __name__ == '__main__':
    main()

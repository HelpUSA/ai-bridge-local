#!/usr/bin/env python3
import sqlite3
import subprocess
import sys
from pathlib import Path

DB_PATH = 'queue_local.db'
INCLUDE_PREFIX = 'ai_bridge_local_'
EXCLUDE_PREFIXES = ['ai_bridge_local_pizza_']

def run_capture(cmd):
    try:
        cp = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        return cp.returncode, cp.stdout.strip(), cp.stderr.strip()
    except Exception as exc:
        return 999, '', str(exc)

def print_block(title, text):
    print('SECTION|' + title)
    if text:
        print(text)
    else:
        print('EMPTY')

def build_filter():
    where = ['command_id like ?']
    params = [INCLUDE_PREFIX + '%']
    for excluded in EXCLUDE_PREFIXES:
        where.append('command_id not like ?')
        params.append(excluded + '%')
    return ' where ' + ' and '.join(where), params

def main():
    print('AI_BRIDGE_LOCAL_HEALTH_START')

    code, out, err = run_capture(['git', 'status', '-sb'])
    print('GIT_STATUS_CODE|' + str(code))
    print_block('git_status', out)
    if err:
        print_block('git_status_stderr', err)

    code, out, err = run_capture(['git', 'log', '--oneline', '-5'])
    print('GIT_LOG_CODE|' + str(code))
    print_block('git_log', out)

    code, out, err = run_capture(['git', 'tag', '--list', 'v0.4.*', '--sort=-creatordate'])
    print('GIT_TAGS_CODE|' + str(code))
    print_block('git_tags', out)

    db_ok = Path(DB_PATH).exists()
    print('DB_EXISTS|' + str(db_ok))
    if db_ok:
        clause, params = build_filter()
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        print('DB_FILTER|prefix=' + INCLUDE_PREFIX + '|exclude_prefix=' + ','.join(EXCLUDE_PREFIXES))
        print('DB_FILTERED_COUNTS')
        for row in cur.execute('select status,count(*) from commands' + clause + ' group by status order by status', params).fetchall():
            print(str(row[0]) + '|' + str(row[1]))
        print('DB_RECENT_AI_BRIDGE_LOCAL')
        rows = cur.execute(
            'select id,command_id,action,status,return_code,conversation_id,created_at from commands'
            + clause + ' order by id desc limit 10',
            params,
        ).fetchall()
        for row in rows:
            print('|'.join('' if x is None else str(x)[:160] for x in row))
        con.close()

    code, out, err = run_capture([sys.executable, 'scripts/watcher/ai_bridge_local_cleanup_watcher_scripts.py', '--keep', '30'])
    print('CLEANUP_DRY_RUN_CODE|' + str(code))
    print_block('cleanup_dry_run', out)
    if err:
        print_block('cleanup_dry_run_stderr', err)

    code, out, err = run_capture(['git', 'diff', '--check'])
    print('DIFF_CHECK_CODE|' + str(code))
    print_block('diff_check', out)
    if err:
        print_block('diff_check_stderr', err)

    overall = 'OK' if code == 0 and db_ok else 'WARN'
    print('HEALTH_RESULT|' + overall)
    print('AI_BRIDGE_LOCAL_HEALTH_END')
    if overall != 'OK':
        sys.exit(1)

if __name__ == '__main__':
    main()

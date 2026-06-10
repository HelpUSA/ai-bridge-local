#!/usr/bin/env python3
import sqlite3

DB_PATH = "queue_local.db"

def main():
    print("AI_BRIDGE_LOCAL_DB_STATUS_START")
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    print("STATUS_COUNTS")
    for status, count in cur.execute(
        "select status, count(*) from commands group by status order by status"
    ).fetchall():
        print(f"{status}|{count}")

    print("RECENT_COMMANDS")
    rows = cur.execute(
        "select id, command_id, action, status, return_code, created_at "
        "from commands order by id desc limit 30"
    ).fetchall()
    for row in rows:
        print("|".join("" if x is None else str(x)[:160] for x in row))

    con.close()
    print("AI_BRIDGE_LOCAL_DB_STATUS_END")

if __name__ == "__main__":
    main()

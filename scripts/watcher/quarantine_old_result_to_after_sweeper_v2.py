import sqlite3
from datetime import datetime, timezone

DB = "queue_local.db"
MAX_AGE_SECONDS = 6 * 60 * 60

def parse_dt(v):
    if not v:
        return None
    s = str(v).strip()
    if not s:
        return None
    try:
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        return datetime.fromisoformat(s)
    except Exception:
        return None

def age_seconds(row):
    for idx in (7, 6, 5):
        if idx < len(row):
            dt = parse_dt(row[idx])
            if dt:
                return max(0, int((datetime.now(timezone.utc) - dt.astimezone(timezone.utc)).total_seconds()))
    return 999999

conn = sqlite3.connect(DB)
cols = [r[1] for r in conn.execute("pragma table_info(commands)").fetchall()]
colset = set(cols)

select_cols = ["id","command_id","action","status","source_chat_id","target_chat_id"]
for c in ("created_at","updated_at","acked_at"):
    if c in colset:
        select_cols.append(c)

sql = "select " + ",".join(select_cols) + " from commands where command_id like 'result_to_%' and status='queued' order by id desc"
rows = conn.execute(sql).fetchall()

to_quarantine = []
for r in rows:
    age = age_seconds(r)
    cid = r[1]
    if age > MAX_AGE_SECONDS:
        to_quarantine.append((r, age))

print("OLD_RESULT_TO_QUARANTINE")
print("queued_result_to_count=" + str(len(rows)))
print("old_result_to_count=" + str(len(to_quarantine)))

for r, age in to_quarantine[:100]:
    print((r[0], r[1], r[3], r[5], age))

for r, age in to_quarantine:
    rid = r[0]
    updates = {"status": "failed"}
    if "last_error" in colset:
        updates["last_error"] = "quarantined_old_result_to_after_sweeper_v2"
    if "stderr" in colset:
        updates["stderr"] = "quarantined_old_result_to_after_sweeper_v2"
    if "updated_at" in colset:
        updates["updated_at"] = datetime.now(timezone.utc).isoformat()

    sets = ", ".join([k + "=?" for k in updates])
    vals = list(updates.values()) + [rid]
    conn.execute("update commands set " + sets + " where id=?", vals)

conn.commit()

print("APPLIED_OLD_RESULT_TO_QUARANTINE=" + str(len(to_quarantine)))

print("RECENT_RESULT_TO_AFTER")
for r in conn.execute("select id,command_id,status,source_chat_id,target_chat_id from commands where command_id like 'result_to_%' order by id desc limit 40").fetchall():
    print(r)

conn.close()

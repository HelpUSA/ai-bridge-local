import argparse
import sqlite3
from datetime import datetime, timezone

BAD_TARGETS = {"", "unknown", "none", "null", "gateway-brain-supervisor"}

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def lower(v):
    return str(v or "").lower()

def row_get(row, key, default=None):
    try:
        return row[key]
    except Exception:
        return default

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
    for k in ("updated_at", "acked_at", "created_at", "inserted_at"):
        dt = parse_dt(row_get(row, k))
        if dt:
            return max(0, int((datetime.now(timezone.utc) - dt.astimezone(timezone.utc)).total_seconds()))
    return 999999

def is_internal_notice(command_id):
    cid = str(command_id or "")
    return (
        cid.startswith("local_status_accepted_") or
        cid.startswith("local_status_delivery_")
    )

def is_true_final_result(row):
    cid = str(row_get(row, "command_id", "") or "")
    action = str(row_get(row, "action", "") or "")

    if action != "send-chat-message":
        return False

    if is_internal_notice(cid):
        return False

    if cid.startswith("result_to_"):
        return True

    blob = "\n".join([
        str(row_get(row, "message", "") or ""),
        str(row_get(row, "payload", "") or ""),
        str(row_get(row, "payload_json", "") or ""),
    ]).lower()

    return "[ai_local_run]" in blob or ("result_is_final" in blob and "chat_can_continue" in blob)

def origin_from_result_id(command_id):
    cid = str(command_id or "")
    if cid.startswith("result_to_"):
        return cid[len("result_to_"):]
    return ""

def update_row(conn, cols, row_id, updates, dry_run):
    updates = {k: v for k, v in updates.items() if k in cols}
    if not updates:
        return False

    if dry_run:
        return True

    sets = ", ".join([k + "=?" for k in updates.keys()])
    vals = list(updates.values())
    vals.append(row_id)
    conn.execute("update commands set " + sets + " where id=?", vals)
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="queue_local.db")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--min-age-seconds", type=int, default=45)
    ap.add_argument("--max-age-seconds", type=int, default=7200)
    ap.add_argument("--cleanup-internal", action="store_true")
    args = ap.parse_args()

    dry_run = not args.apply

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row

    cols = [r[1] for r in conn.execute("pragma table_info(commands)").fetchall()]
    rows = conn.execute("select * from commands order by id desc limit 3000").fetchall()

    run_by_command_id = {}
    for row in rows:
        if str(row_get(row, "action", "") or "") == "run-command":
            run_by_command_id[str(row_get(row, "command_id", "") or "")] = row

    fixed = []
    suppressed = []
    stale_skipped = 0

    if args.cleanup_internal:
        for row in rows:
            cid = str(row_get(row, "command_id", "") or "")
            status = lower(row_get(row, "status", ""))
            row_age = age_seconds(row)

            if str(row_get(row, "action", "") or "") != "send-chat-message":
                continue
            if not is_internal_notice(cid):
                continue
            if status not in {"queued", "failed", "error", "retry", "pending", "delivering"}:
                continue
            if row_age < args.min_age_seconds:
                continue

            updates = {"status": "acked"}
            if "stdout" in cols:
                updates["stdout"] = "suppressed_internal_notice_by_final_result_sweeper_v3"
            if "last_error" in cols:
                updates["last_error"] = None
            if "stderr" in cols:
                updates["stderr"] = None
            if "updated_at" in cols:
                updates["updated_at"] = now_iso()

            update_row(conn, cols, row_get(row, "id"), updates, dry_run)
            suppressed.append((row_get(row, "id"), cid, status, row_age))

    for row in rows:
        if not is_true_final_result(row):
            continue

        row_age = age_seconds(row)

        if row_age < args.min_age_seconds:
            continue

        if row_age > args.max_age_seconds:
            stale_skipped += 1
            continue

        rid = row_get(row, "id")
        cid = str(row_get(row, "command_id", "") or "")
        status = lower(row_get(row, "status", ""))
        target = str(row_get(row, "target_chat_id", "") or "")
        target_low = lower(target)

        updates = {}

        origin_id = origin_from_result_id(cid)
        origin = run_by_command_id.get(origin_id)

        if target_low in BAD_TARGETS and origin is not None:
            origin_source = str(row_get(origin, "source_chat_id", "") or "")
            if lower(origin_source) not in BAD_TARGETS:
                updates["target_chat_id"] = origin_source

        if status in {"failed", "error", "retry", "pending", "delivering"}:
            updates["status"] = "queued"
        elif status == "queued" and target_low in BAD_TARGETS:
            updates["status"] = "queued"

        if updates:
            if "last_error" in cols:
                updates["last_error"] = None
            if "stderr" in cols:
                updates["stderr"] = None
            if "updated_at" in cols:
                updates["updated_at"] = now_iso()

            update_row(conn, cols, rid, updates, dry_run)
            fixed.append((rid, cid, status, target, row_age, updates))

    if not dry_run:
        conn.commit()

    print("FINAL_RESULT_SWEEPER_V3")
    print("mode=" + ("APPLY" if args.apply else "DRY_RUN"))
    print("true_final_fixed=" + str(len(fixed)))
    print("internal_suppressed=" + str(len(suppressed)))
    print("stale_true_final_skipped=" + str(stale_skipped))

    print("FIXED")
    for item in fixed[:80]:
        print(item)

    print("RECENT_RESULT_ROWS")
    q = """
    select id, command_id, action, status, source_chat_id, target_chat_id
    from commands
    where command_id like 'result_to_%'
       or command_id like 'local_status_accepted_result_to_%'
    order by id desc
    limit 40
    """
    for item in conn.execute(q).fetchall():
        print(tuple(item))

    conn.close()

if __name__ == "__main__":
    main()

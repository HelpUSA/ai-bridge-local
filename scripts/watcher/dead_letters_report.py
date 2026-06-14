import argparse
import json
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "queue_local.db"

parser = argparse.ArgumentParser(description="Grouped dead letters report for AI Bridge Local")
parser.add_argument("--limit", type=int, default=20)
parser.add_argument("--prefix", default="ai_bridge_local")
parser.add_argument("--target", default="")
parser.add_argument("--json", action="store_true")
args = parser.parse_args()

limit = max(1, min(args.limit, 100))

def classify_error(text):
    t = (text or "").lower()
    if "indentationerror" in t:
        return "python_indentation"
    if "syntaxerror" in t:
        return "python_syntax"
    if "json" in t or "parse" in t or "escaped" in t or "unterminated" in t:
        return "json_parse"
    if "diff_check" in t or "whitespace" in t:
        return "diff_check"
    if "validate_all" in t:
        return "validate_all"
    if "release_check" in t:
        return "release_check"
    if "timeout" in t:
        return "timeout"
    if "pathspec" in t or "did not match any file" in t:
        return "git_pathspec"
    if "return_code" in t or "returned non-zero" in t:
        return "command_failed"
    if not t.strip():
        return "empty_error"
    return "other"

def project_from_command(command_id):
    cid = command_id or ""
    if cid.startswith("ai_bridge_local"):
        return "ai_bridge_local"
    if cid.startswith("pizza"):
        return "pizza"
    if cid.startswith("helpus"):
        return "helpus"
    if cid.startswith("trading"):
        return "trading"
    return cid.split("_")[0] if cid else "unknown"

def clipped(text, size=500):
    value = str(text or "")
    return value if len(value) <= size else value[:size] + "...[clipped]"

def print_safe(obj):
    print(str(obj).encode("ascii", "backslashreplace").decode("ascii"))

def increment(bucket, key):
    bucket[key] = bucket.get(key, 0) + 1

def top_items(bucket):
    return sorted(bucket.items(), key=lambda x: (-x[1], str(x[0])))[:limit]

if not DB.exists():
    payload = {"ok": False, "status": "db_not_found", "db": str(DB)}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("AI_BRIDGE_LOCAL_DEAD_LETTERS_GROUPED_REPORT")
        print_safe(payload)
    raise SystemExit(2)

where = []
params = []
if args.prefix:
    where.append("command_id like ?")
    params.append(args.prefix + "%")
if args.target:
    where.append("target_chat_id=?")
    params.append(args.target)
sql_where = (" where " + " and ".join(where)) if where else ""

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
rows = list(con.execute("select id, command_id, target_chat_id, last_error, failed_at from dead_letters" + sql_where, params))

by_error_kind = {}
by_project = {}
by_target = {}
by_command_id = {}
by_target_and_kind = {}

for row in rows:
    kind = classify_error(row["last_error"])
    target = row["target_chat_id"] or "unknown"
    command_id = row["command_id"] or "unknown"
    project = project_from_command(command_id)
    increment(by_error_kind, kind)
    increment(by_project, project)
    increment(by_target, target)
    increment(by_command_id, command_id)
    increment(by_target_and_kind, target + " | " + kind)

recent_params = list(params)
recent_params.append(limit)
recent_sql = "select id, command_id, target_chat_id, last_error, failed_at from dead_letters" + sql_where + " order by id desc limit ?"
recent = []
for row in con.execute(recent_sql, recent_params):
    item = dict(row)
    item["error_kind"] = classify_error(item.get("last_error"))
    item["project"] = project_from_command(item.get("command_id"))
    item["last_error"] = clipped(item.get("last_error"))
    recent.append(item)

payload = {
    "ok": True,
    "schema": "ai_bridge_local.dead_letters_grouped_report",
    "schema_version": 2,
    "filters": {"prefix": args.prefix, "target": args.target, "limit": limit},
    "total": len(rows),
    "by_error_kind": [{"kind": k, "n": n} for k, n in top_items(by_error_kind)],
    "by_project": [{"project": k, "n": n} for k, n in top_items(by_project)],
    "by_target": [{"target": k, "n": n} for k, n in top_items(by_target)],
    "by_command_id": [{"command_id": k, "n": n} for k, n in top_items(by_command_id)],
    "by_target_and_kind": [{"target_and_kind": k, "n": n} for k, n in top_items(by_target_and_kind)],
    "recent_filtered": recent,
}
con.close()

if args.json:
    print(json.dumps(payload, indent=2, sort_keys=True))
else:
    print("AI_BRIDGE_LOCAL_DEAD_LETTERS_GROUPED_REPORT")
    print("filters")
    print_safe(payload["filters"])
    print("total")
    print_safe(payload["total"])
    for section in ["by_error_kind", "by_project", "by_target", "by_command_id", "by_target_and_kind", "recent_filtered"]:
        print(section)
        for item in payload[section]:
            print_safe(item)

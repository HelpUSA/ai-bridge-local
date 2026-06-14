import argparse
import json
import sqlite3
from pathlib import Path


def quote_ident(name):
    return "[" + str(name).replace("]", "]]") + "]"


def inspect_db(path):
    result = {
        "db": str(path),
        "exists": path.exists(),
        "status_counts": {},
        "warnings": [],
    }
    if not path.exists():
        result["warnings"].append("db_missing")
        return result

    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    try:
        rows = con.execute(
            "select name from sqlite_master where type = ?",
            ("table",),
        ).fetchall()
        for row in rows:
            table = row[0]
            cols = [
                col[1]
                for col in con.execute("pragma table_info(" + quote_ident(table) + ")")
            ]
            if "status" not in cols:
                continue
            sql = "select status, count(*) as n from " + quote_ident(table) + " group by status"
            counts = {
                str(item["status"]): int(item["n"])
                for item in con.execute(sql)
            }
            result["status_counts"][table] = counts
    finally:
        con.close()

    for counts in result["status_counts"].values():
        if counts.get("queued", 0) > 0:
            result["warnings"].append("queued_commands_present")
        if counts.get("delivering", 0) > 0:
            result["warnings"].append("delivering_commands_present")
        if counts.get("failed", 0) > 0:
            result["warnings"].append("failed_commands_present")

    result["warnings"] = sorted(set(result["warnings"]))
    return result


def find_default_db(root):
    candidates = [
        p
        for p in root.rglob("*.db")
        if ".git" not in p.parts
    ]
    candidates.sort(key=lambda p: p.stat().st_size if p.exists() else 0, reverse=True)
    return candidates[0] if candidates else root / "missing.db"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path.cwd()
    db_path = Path(args.db) if args.db else find_default_db(root)
    result = inspect_db(db_path)
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print("AI_BRIDGE_LOCAL_QUEUE_HEALTH_AUDIT")
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

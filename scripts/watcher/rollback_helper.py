import argparse
import json
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description="Safe rollback helper for AI Bridge Local")
parser.add_argument("--cwd", default=".")
parser.add_argument("--path", action="append", default=[])
parser.add_argument("--restore", action="store_true")
parser.add_argument("--delete-untracked", action="store_true")
parser.add_argument("--confirm-delete-untracked", action="append", default=[])
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()

root = Path(args.cwd).resolve()
result = {
    "schema": "ai_bridge_local.rollback_helper",
    "schema_version": 1,
    "cwd": str(root),
    "dry_run": bool(args.dry_run),
}

def emit(code=0):
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(code)

def run(cmd):
    return subprocess.run(cmd, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if not root.exists():
    result.update({"ok": False, "status": "invalid_cwd"})
    emit(2)

status = run(["git", "status", "--porcelain=v1"])
if status.returncode != 0:
    result.update({"ok": False, "status": "git_status_failed", "stderr": status.stderr[-2000:]})
    emit(1)

entries = []
status_by_path = {}
for raw in status.stdout.splitlines():
    if not raw:
        continue
    code = raw[:2]
    path = raw[3:]
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    kind = "untracked" if code == "??" else "tracked_modified"
    item = {"path": path, "code": code, "kind": kind}
    entries.append(item)
    status_by_path[path] = item

result["changes"] = entries
selected = list(args.path)
result["selected_paths"] = selected

if not args.restore and not args.delete_untracked:
    result.update({
        "ok": True,
        "status": "plan",
        "restore_candidates": [x for x in entries if x["kind"] == "tracked_modified"],
        "untracked_candidates": [x for x in entries if x["kind"] == "untracked"],
    })
    emit(0)

if not selected:
    result.update({"ok": False, "status": "no_paths_selected"})
    emit(2)

confirmed_untracked = set(args.confirm_delete_untracked)
actions = []
for path in selected:
    resolved = (root / path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        result.update({"ok": False, "status": "path_outside_cwd", "path": path})
        emit(2)

    item = status_by_path.get(path)
    if item is None:
        actions.append({"path": path, "action": "skip_clean_or_missing"})
        continue

    if item["kind"] == "tracked_modified":
        if args.restore:
            if args.dry_run:
                actions.append({"path": path, "action": "would_restore_tracked"})
            else:
                cp = run(["git", "restore", "--", path])
                actions.append({"path": path, "action": "restore_tracked", "return_code": cp.returncode, "stderr": cp.stderr[-2000:]})
                if cp.returncode != 0:
                    result.update({"ok": False, "status": "restore_failed", "actions": actions})
                    emit(1)
        else:
            actions.append({"path": path, "action": "skip_tracked_restore_not_requested"})
    elif item["kind"] == "untracked":
        confirmed = path in confirmed_untracked
        if args.delete_untracked and confirmed:
            if args.dry_run:
                actions.append({"path": path, "action": "would_delete_untracked"})
            else:
                target = root / path
                if target.is_dir():
                    result.update({"ok": False, "status": "refuse_delete_directory", "path": path, "actions": actions})
                    emit(2)
                target.unlink(missing_ok=True)
                actions.append({"path": path, "action": "delete_untracked"})
        else:
            actions.append({"path": path, "action": "refuse_untracked_without_explicit_confirmation"})

result.update({"ok": True, "status": "dry_run" if args.dry_run else "completed", "actions": actions})
emit(0)

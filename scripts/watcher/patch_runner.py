import argparse
import json
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description="Safe git patch runner for AI Bridge Local")
parser.add_argument("--patch-file", required=True)
parser.add_argument("--cwd", default=".")
parser.add_argument("--dry-run", action="store_true")
parser.add_argument("--apply", action="store_true")
args = parser.parse_args()

root = Path(args.cwd).resolve()
raw_patch = Path(args.patch_file)
patch = raw_patch.resolve() if raw_patch.is_absolute() else (root / raw_patch).resolve()
result = {
    "schema": "ai_bridge_local.patch_runner",
    "schema_version": 1,
    "cwd": str(root),
    "patch_file": str(patch),
    "apply_requested": bool(args.apply),
}

def emit(code=0):
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(code)

if not root.exists():
    result.update({"ok": False, "status": "invalid_cwd"})
    emit(2)

if patch.suffix.lower() not in {".patch", ".diff"}:
    result.update({"ok": False, "status": "unsupported_patch_suffix"})
    emit(2)

try:
    patch.relative_to(root)
except ValueError:
    result.update({"ok": False, "status": "patch_outside_cwd"})
    emit(2)

if not patch.exists():
    result.update({"ok": False, "status": "patch_file_not_found"})
    emit(2)

text = patch.read_text(encoding="utf-8", errors="replace")
if chr(0) in text:
    result.update({"ok": False, "status": "binary_patch_rejected"})
    emit(2)

check_cmd = ["git", "apply", "--check", "--whitespace=error-all", str(patch)]
check = subprocess.run(check_cmd, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
result.update({
    "check_return_code": check.returncode,
    "check_stdout": check.stdout[-2000:],
    "check_stderr": check.stderr[-2000:],
})
if check.returncode != 0:
    result.update({"ok": False, "status": "check_failed"})
    emit(1)

if args.dry_run or not args.apply:
    result.update({"ok": True, "status": "dry_run_ok" if args.dry_run else "checked", "applied": False})
    emit(0)

apply_cmd = ["git", "apply", "--whitespace=error-all", str(patch)]
applied = subprocess.run(apply_cmd, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
result.update({
    "apply_return_code": applied.returncode,
    "apply_stdout": applied.stdout[-2000:],
    "apply_stderr": applied.stderr[-2000:],
})
if applied.returncode != 0:
    result.update({"ok": False, "status": "apply_failed", "applied": False})
    emit(1)

result.update({"ok": True, "status": "applied", "applied": True})
emit(0)

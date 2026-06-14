import json
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
cmd = [
    sys.executable,
    str(ROOT / "scripts" / "watcher" / "dead_letters_report.py"),
    "--limit",
    "3",
    "--prefix",
    "ai_bridge_local",
]
proc = subprocess.run(cmd, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=30)
out = proc.stdout + proc.stderr
assert proc.returncode == 0, out
for needed in [
    "AI_BRIDGE_LOCAL_DEAD_LETTERS_GROUPED_REPORT",
    "by_error_kind",
    "by_project",
    "by_target",
    "by_command_id",
    "by_target_and_kind",
    "recent_filtered",
]:
    assert needed in out, out

json_cmd = cmd + ["--json"]
proc = subprocess.run(json_cmd, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=30)
out = proc.stdout + proc.stderr
assert proc.returncode == 0, out
data = json.loads(proc.stdout)
assert data["schema"] == "ai_bridge_local.dead_letters_grouped_report", data
assert data["schema_version"] == 2, data
assert "by_error_kind" in data and "by_command_id" in data and "recent_filtered" in data, data
print("OK dead_letters_report_smoke")

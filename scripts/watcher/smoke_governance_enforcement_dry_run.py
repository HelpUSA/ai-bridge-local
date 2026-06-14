import json
import subprocess
import sys
from pathlib import Path


ROOT = Path.cwd()
tool = ROOT / "scripts" / "watcher" / "governance_enforcement_dry_run.py"


def run_case(command):
    cmd = [sys.executable, str(tool), "--json", "--command"] + command
    run = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return json.loads(run.stdout)


destructive = run_case(["Remove-Item", "temp", "-Recurse", "-Force"])
assert destructive["risk_level"] == "destructive"
assert destructive["would_block_if_enforced"] is True
assert destructive["blocks_execution_now"] is False

read_only = run_case(["git", "status", "-sb"])
assert read_only["risk_level"] == "read_only_or_dry_run"
assert read_only["would_block_if_enforced"] is False
assert read_only["blocks_execution_now"] is False

mutating = run_case(["Set-Content", "file.txt", "value"])
assert mutating["risk_level"] == "mutating"
assert mutating["would_block_if_enforced"] is False
assert mutating["blocks_execution_now"] is False

print("OK governance_enforcement_dry_run_smoke")

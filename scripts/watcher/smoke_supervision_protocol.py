
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
cmd = [sys.executable, str(ROOT / "scripts" / "watcher" / "supervision_protocol.py")]

proc = subprocess.run(cmd, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=30)
out = proc.stdout + proc.stderr
assert proc.returncode == 0, out
for needed in [
    "AI_BRIDGE_LOCAL_SUPERVISION_PROTOCOL",
    "roles",
    "gates",
    "phases",
    "phase plan",
    "phase readonly",
    "phase patch",
    "phase release",
    "phase handoff",
]:
    assert needed in out, out

json_proc = subprocess.run(cmd + ["--json"], cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=30)
json_out = json_proc.stdout + json_proc.stderr
assert json_proc.returncode == 0, json_out
data = json.loads(json_proc.stdout)
assert data["schema"] == "ai_bridge_local.supervision_protocol", data
assert data["schema_version"] == 1, data
assert len(data["phases"]) == 5, data
assert "no_patch_before_readonly" in data["gates"], data

phase_proc = subprocess.run(cmd + ["--phase", "patch", "--json"], cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=30)
phase_out = phase_proc.stdout + phase_proc.stderr
assert phase_proc.returncode == 0, phase_out
phase_data = json.loads(phase_proc.stdout)
assert len(phase_data["phases"]) == 1 and phase_data["phases"][0]["phase"] == "patch", phase_data
print("OK supervision_protocol_smoke")

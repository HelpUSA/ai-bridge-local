from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path.cwd()
STATE_DIR = ROOT / "runtime" / "smart_tasks"
STATE = STATE_DIR / "smoke_smart_task.json"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


if STATE.exists():
    STATE.unlink()

run(["python", "scripts/watcher/smart_task_runner.py", "demo", "--dry-run", "--task-id", "smoke_smart_task"])

dry = json.loads(STATE.read_text(encoding="utf-8"))
assert dry["status"] == "planned", dry
assert [step["name"] for step in dry["steps"]] == ["inspect", "plan", "validate"], dry
assert all(not step["completed"] for step in dry["steps"]), dry
assert all(step["output"] == "planned" for step in dry["steps"]), dry

run(["python", "scripts/watcher/smart_task_runner.py", "demo", "--task-id", "smoke_smart_task"])

done = json.loads(STATE.read_text(encoding="utf-8"))
assert done["status"] == "completed", done
assert all(step["completed"] for step in done["steps"]), done
assert done["last_error"] == "", done

catalog = json.loads(run(["python", "scripts/watcher/smart_task_runner.py", "--catalog"]).stdout)
task_ids = {item["task_id"] for item in catalog}
assert "smart_watcher_demo" in task_ids, catalog
assert "docs_v0_update" in task_ids, catalog
assert "release_validation" in task_ids, catalog

diag = json.loads(
    run(
        [
            "python",
            "scripts/watcher/smart_task_runner.py",
            "--classify-error",
            "Expected ',' after property value in JSON",
            "--json",
        ]
    ).stdout
)
assert diag["category"] == "invalid_json", diag
assert diag["retryable"] is True, diag

run(["python", "-m", "py_compile", "scripts/watcher/smart_task_runner.py", "scripts/watcher/safe_ops.py"])

if STATE.exists():
    STATE.unlink()

if STATE_DIR.exists() and not any(STATE_DIR.iterdir()):
    STATE_DIR.rmdir()

runtime = ROOT / "runtime"
if runtime.exists() and not any(runtime.iterdir()):
    runtime.rmdir()

print("OK smoke_smart_task_runner")

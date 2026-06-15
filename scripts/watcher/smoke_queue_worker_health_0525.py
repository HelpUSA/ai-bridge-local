from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "watcher"))

from queue_worker_health import (  # noqa: E402
    build_queue_worker_health_snapshot,
    render_queue_worker_health,
)

def version_tuple(value):
    return tuple(int(part) for part in value.split("."))

VERSION = (ROOT / "VERSION").read_text(encoding="utf-8-sig").strip()
assert version_tuple(VERSION) >= version_tuple("0.5.25"), VERSION

snapshot = {
    "commands": [
        {"status": "queued"},
        {"status": "failed"},
        {"status": "acked"},
    ],
    "workers": [
        {"id": "w1", "state": "running"},
        {"id": "w2", "state": "active"},
    ],
    "locks": [
        {"id": "lock-1", "state": "stale"},
    ],
}

health = build_queue_worker_health_snapshot(snapshot)
assert health["readonly"] is True
assert health["command_total"] == 3
assert health["by_status"]["queued"] == 1
assert health["by_status"]["failed"] == 1
assert health["worker_total"] == 2
assert health["active_worker_count"] == 2
assert health["duplicate_active_workers"] == 1
assert health["stale_lock_count"] == 1
assert "duplicate_active_workers" in health["warnings"]
assert "stale_locks_present" in health["warnings"]
assert "failed_commands_present" in health["warnings"]
assert health["healthy"] is False

rendered = render_queue_worker_health(health)
assert "# Queue worker health" in rendered
assert "readonly=true" in rendered
assert "- duplicate_active_workers" in rendered

doc = (ROOT / "docs" / "QUEUE_WORKER_HEALTH_0525.md").read_text(encoding="utf-8-sig")
guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")
assert "Queue worker health 0.5.25" in doc
assert "nao executa entrega inter-chat" in doc
assert "Queue worker health 0.5.25" in guide

print("OK queue_worker_health_0525 " + VERSION)
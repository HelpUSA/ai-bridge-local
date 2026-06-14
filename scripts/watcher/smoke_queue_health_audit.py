import json
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path.cwd()
db = Path(tempfile.mkdtemp()) / "queue.db"

con = sqlite3.connect(db)
con.execute("create table messages (id integer primary key, status text)")
con.executemany(
    "insert into messages(status) values (?)",
    [("acked",), ("queued",), ("failed",), ("delivering",)],
)
con.commit()
con.close()

cmd = [
    sys.executable,
    str(ROOT / "scripts" / "watcher" / "queue_health_audit.py"),
    "--db",
    str(db),
    "--json",
]
run = subprocess.run(
    cmd,
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    check=True,
)
data = json.loads(run.stdout)
counts = data["status_counts"]["messages"]

assert counts["acked"] == 1
assert counts["queued"] == 1
assert counts["failed"] == 1
assert counts["delivering"] == 1
assert "queued_commands_present" in data["warnings"]
assert "delivering_commands_present" in data["warnings"]
assert "failed_commands_present" in data["warnings"]

print("OK queue_health_audit_smoke")

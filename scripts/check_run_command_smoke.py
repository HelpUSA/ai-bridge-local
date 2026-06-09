import sqlite3
from pathlib import Path

db = Path("D:/dev/autocode/ai-bridge-local/queue_local.db")
cmd_id = "run_command_local_smoke_001"

conn = sqlite3.connect(str(db))
conn.row_factory = sqlite3.Row

print("===== RUN-COMMAND STATUS =====")
row = conn.execute("""
    SELECT id, command_id, action, target_chat_id, status, delivered_at, acked_at, return_code, stdout, stderr, last_error
    FROM commands
    WHERE command_id=?
""", (cmd_id,)).fetchone()

if row:
    d = dict(row)
    for k, v in d.items():
        print(f"{k}: {v}")
else:
    print("NOT_FOUND")

print("\n===== STATUS COUNTS =====")
for r in conn.execute("SELECT status, COUNT(*) AS c FROM commands GROUP BY status ORDER BY c DESC"):
    print(r["status"], r["c"])

conn.close()

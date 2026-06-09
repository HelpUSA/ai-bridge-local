import sqlite3
from pathlib import Path

db = Path("D:/dev/autocode/ai-bridge-local/queue_local.db")

print("===== SQLITE QUEUE SUMMARY =====")
print("DB_EXISTS=", db.exists(), "SIZE=", db.stat().st_size if db.exists() else 0)

conn = sqlite3.connect(str(db))
conn.row_factory = sqlite3.Row

print("\nTABLES:")
for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    print("-", row["name"])

print("\nCOMMANDS BY STATUS:")
for row in conn.execute("SELECT status, COUNT(*) AS c FROM commands GROUP BY status ORDER BY c DESC"):
    print(row["status"], row["c"])

print("\nRECENT COMMANDS:")
rows = conn.execute("""
    SELECT id, command_id, action, source_chat_id, target_chat_id, status, created_at, delivered_at, acked_at
    FROM commands
    ORDER BY id DESC
    LIMIT 20
""").fetchall()

for r in rows:
    print(dict(r))

conn.close()

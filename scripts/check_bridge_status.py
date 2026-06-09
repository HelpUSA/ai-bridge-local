import sqlite3
from pathlib import Path

db = Path("D:/dev/autocode/ai-bridge-local/queue_local.db")

conn = sqlite3.connect(str(db))
conn.row_factory = sqlite3.Row

print("===== STATUS COUNTS =====")
for r in conn.execute("SELECT status, COUNT(*) AS c FROM commands GROUP BY status ORDER BY c DESC"):
    print(r["status"], r["c"])

print("\n===== LAST 12 COMMANDS =====")
rows = conn.execute("""
    SELECT id, command_id, action, source_chat_id, target_chat_id, status, created_at, delivered_at, acked_at
    FROM commands
    ORDER BY id DESC
    LIMIT 12
""").fetchall()

for r in rows:
    print(dict(r))

print("\n===== RECENT EVENTS =====")
try:
    rows = conn.execute("""
        SELECT id, command_id, event_type, message, payload_json, created_at
        FROM events
        ORDER BY id DESC
        LIMIT 20
    """).fetchall()
    for r in rows:
        print(dict(r))
except Exception as e:
    print("EVENTS_READ_ERROR", repr(e))

conn.close()

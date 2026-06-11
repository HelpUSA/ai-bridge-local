from pathlib import Path

p = Path("gateway_local.py")
txt = p.read_text(encoding="utf-8-sig")

txt = txt.replace('"version": "0.2.1"', '"version": "0.2.2"')
txt = txt.replace('version": "0.2.1"', 'version": "0.2.2"')

if "def fail_stale_deliveries" not in txt:
    marker = "def fetch_control_status():"
    idx = txt.index(marker)
    helper = '''def fail_stale_deliveries(max_age_seconds=45):
    """Fail inter-chat commands that were delivered to the extension but never acked."""
    cutoff_expr = f"-{int(max_age_seconds)} seconds"
    with get_conn() as conn:
        conn.execute(
            """
            UPDATE commands
               SET status='failed',
                   acked_at=?,
                   last_error='stale delivering timeout after extension delivery',
                   stderr='stale delivering timeout after extension delivery'
             WHERE status='delivering'
               AND action IN ('send-message','send-chat-message')
               AND delivered_at IS NOT NULL
               AND datetime(substr(delivered_at, 1, 19)) < datetime('now', ?)
            """,
            (now_iso(), cutoff_expr),
        )
        conn.commit()

'''
    txt = txt[:idx] + helper + txt[idx:]

if "fail_stale_deliveries()" not in txt:
    txt = txt.replace(
        "def fetch_control_status():\n",
        "def fetch_control_status():\n    fail_stale_deliveries()\n",
        1,
    )

next_action = 'if self.path.startswith("/bridge/next-action"):'
if next_action in txt and "fail_stale_deliveries()\n" not in txt[txt.index(next_action)-120:txt.index(next_action)+120]:
    txt = txt.replace(
        next_action,
        'if self.path.startswith("/bridge/next-action"):\n            fail_stale_deliveries()',
        1,
    )

p.write_text(txt, encoding="utf-8")

print("PATCH_GATEWAY_WATCHDOG_DONE")

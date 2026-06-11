from pathlib import Path

p = Path("gateway_local.py")
txt = p.read_text(encoding="utf-8-sig")

# bump gateway reported version if present
txt = txt.replace('"version": "0.2.1"', '"version": "0.2.3"')
txt = txt.replace('"version": "0.2.2"', '"version": "0.2.3"')
txt = txt.replace("'version': '0.2.1'", "'version': '0.2.3'")
txt = txt.replace("'version': '0.2.2'", "'version': '0.2.3'")

start = txt.find("def fail_stale_deliveries")
end = txt.find("def fetch_control_status")

if start < 0 or end < 0 or end <= start:
    raise SystemExit("Nao encontrei bloco fail_stale_deliveries/fetch_control_status para substituir")

new_func = '''def fail_stale_deliveries(max_age_seconds=45):
    """Fail inter-chat commands that were delivered to the extension but never acked."""
    try:
        cutoff_expr = f"-{int(max_age_seconds)} seconds"
        conn = sqlite3.connect(DB_PATH)
        try:
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
        finally:
            conn.close()
    except Exception as e:
        print("[gateway] fail_stale_deliveries error:", e)

'''

txt = txt[:start] + new_func + txt[end:]

p.write_text(txt, encoding="utf-8")
print("PATCH_GATEWAY_WATCHDOG_023_DONE")

from pathlib import Path
p = Path("extension/content_script.js")
t = p.read_text(encoding="utf-8-sig")
t = t.replace('const VERSION = "0.4.37";', 'const VERSION = "0.4.38";')
old = '''      if (!target || !message) {
        reportEnvelopeError("simple_bridge_missing_fields", "BRIDGE_SEND_CHAT_MESSAGE precisa de target_chat_id e message", raw);
        continue;
      }
'''
new = '''      if (!target || !message) {
        continue;
      }
'''
if old not in t:
    raise SystemExit("MISSING_FIELDS_BLOCK_NOT_FOUND")
t = t.replace(old, new, 1)
p.write_text(t, encoding="utf-8")
print("PATCH_IGNORE_INCOMPLETE_SIMPLE_EXIMPLES_OK")

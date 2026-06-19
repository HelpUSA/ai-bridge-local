from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[2]
content = (root / "extension" / "content_script.js").read_text(encoding="utf-8", errors="replace")
manifest = json.loads((root / "extension" / "manifest.json").read_text(encoding="utf-8", errors="replace"))
version = (root / "VERSION").read_text(encoding="utf-8", errors="replace").strip()

assert version == "0.5.53", version
assert manifest.get("version") == "0.5.53", manifest.get("version")
assert 'const VERSION = "0.5.53";' in content
assert "AI Bridge Local: DeepSeek outbound envelope capture 0.5.53" in content
assert "__AI_BRIDGE_DEEPSEEK_CAPTURE_INSTALLED__" in content
assert "DeepSeek outbound envelope observer installed" in content
assert "chat.deepseek.com" in content or "chat\\.deepseek\\.com" in content
assert "AI_BRIDGE_CAPTURED_ENVELOPE" in content
assert "source_chat_id_mismatch" in content
assert "ai_bridge_source_chat_id_mismatch:" in content
assert "BOOTSTRAP_MS" in content
assert "showNotice(\"success\"" in content

print("OK smoke_deepseek_outbound_envelope_capture_0553")

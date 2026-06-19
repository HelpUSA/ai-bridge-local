from pathlib import Path
import json

root = Path(__file__).resolve().parents[2]
content = (root / "extension" / "content_script.js").read_text(encoding="utf-8", errors="replace")
manifest = json.loads((root / "extension" / "manifest.json").read_text(encoding="utf-8", errors="replace"))
version = (root / "VERSION").read_text(encoding="utf-8", errors="replace").strip()

assert version == "0.5.54", version
assert manifest.get("version") == "0.5.54", manifest.get("version")
assert 'const VERSION = "0.5.54";' in content
assert 'const CAPTURE_VERSION = "0.5.54";' in content
assert "DeepSeek outbound envelope capture with persistent receipt 0.5.54" in content
assert "appendPersistentReceipt" in content
assert "ai-bridge-deepseek-persistent-receipt" in content
assert "envelope capturado e entregue pela extensao" in content
assert "status=sent_direct" in content or "status=\" + directFlag" in content
assert "status=runtime_error" in content
assert "status=rejected" in content
assert "parsed.source_node = sourceNode || null;" in content
assert "AI_BRIDGE_CAPTURED_ENVELOPE" in content

print("OK smoke_deepseek_persistent_delivery_receipt_0554")

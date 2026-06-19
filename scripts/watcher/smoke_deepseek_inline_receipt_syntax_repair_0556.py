from pathlib import Path
import json

root = Path(__file__).resolve().parents[2]
content = (root / "extension" / "content_script.js").read_text(encoding="utf-8", errors="replace")
manifest = json.loads((root / "extension" / "manifest.json").read_text(encoding="utf-8", errors="replace"))
version = (root / "VERSION").read_text(encoding="utf-8", errors="replace").strip()

assert version == "0.5.56", version
assert manifest.get("version") == "0.5.56", manifest.get("version")
assert 'const VERSION = "0.5.56";' in content
assert 'const CAPTURE_VERSION = "0.5.56";' in content
assert 'join("\\n")' in content
assert 'receipt.textContent = title + "\\n" + formatReceiptLines(lines);' in content
assert "findDeepSeekEnvelopeAnchor" in content
assert "insertReceiptAfterAnchor" in content
assert "DeepSeek inline receipt inserted after envelope" in content
assert "DeepSeek inline receipt anchor not found; used fixed panel" in content
assert "data-ai-bridge-deepseek-receipt" in content
assert "envelope capturado e entregue pela extensao" in content
assert "AI_BRIDGE_CAPTURED_ENVELOPE" in content

print("OK smoke_deepseek_inline_receipt_syntax_repair_0556")

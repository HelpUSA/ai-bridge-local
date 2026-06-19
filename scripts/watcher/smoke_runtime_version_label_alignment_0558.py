from pathlib import Path
import json

root = Path(__file__).resolve().parents[2]
content = (root / "extension" / "content_script.js").read_text(encoding="utf-8", errors="replace")
background = (root / "extension" / "background.js").read_text(encoding="utf-8", errors="replace")
manifest = json.loads((root / "extension" / "manifest.json").read_text(encoding="utf-8", errors="replace"))
version = (root / "VERSION").read_text(encoding="utf-8", errors="replace").strip()

assert version == "0.5.58", version
assert manifest.get("version") == "0.5.58", manifest.get("version")
assert 'const VERSION = "0.5.58";' in content
assert 'const CAPTURE_VERSION = "0.5.58";' in content
assert "ChatGPT outbound envelope observer installed" in content
assert "ChatGPT candidate scanner" in content
assert "Standalone candidate scan" in content
assert "DeepSeek inline receipt inserted after envelope" in content
assert "envelope capturado e entregue pela extensao" in content
assert len(background.strip()) > 100

for stale in ["0.5.52", "0.5.53", "0.5.54", "0.5.55", "0.5.56", "0.5.57"]:
    assert stale not in content, f"stale version in content_script.js: {stale}"
    assert stale not in background, f"stale version in background.js: {stale}"

print("OK smoke_runtime_version_label_alignment_0558")

from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[2]
content = (root / "extension" / "content_script.js").read_text(encoding="utf-8", errors="replace")
manifest = json.loads((root / "extension" / "manifest.json").read_text(encoding="utf-8", errors="replace"))
version = (root / "VERSION").read_text(encoding="utf-8", errors="replace").strip()

assert version == "0.5.57", version
assert manifest.get("version") == "0.5.57", manifest.get("version")
assert 'const VERSION = "0.5.57";' in content
assert "ChatGPT outbound envelope observer installed" in content
assert "ChatGPT candidate scanner" in content
assert "Standalone candidate scan" in content
assert "processText(text, reason, bootstrapOnly, null);" in content
assert not re.search(r'processText\(\s*text\s*,\s*reason\s*,\s*bootstrapOnly\s*,\s*node\s*\);', content)
assert "[Local v0.5.52]" not in content

print("OK smoke_chatgpt_standalone_scanner_node_scope_0557")

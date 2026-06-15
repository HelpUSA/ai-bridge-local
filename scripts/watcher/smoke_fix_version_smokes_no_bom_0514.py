from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
version_bytes = (ROOT / "VERSION").read_bytes()
assert not version_bytes.startswith(b"\xef\xbb\xbf"), version_bytes
VERSION = version_bytes.decode("utf-8").strip()
assert VERSION == "0.5.14", VERSION

manifest = json.loads((ROOT / "extension" / "manifest.json").read_text(encoding="utf-8-sig"))
assert manifest["version"] == VERSION, manifest
assert VERSION in manifest["name"], manifest["name"]

guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")
doc = (ROOT / "docs" / "FIX_VERSION_SMOKES_NO_BOM_0514.md").read_text(encoding="utf-8-sig")

assert "Version alignment 0.5.14" in guide
assert "Fix version smokes and UTF-8 no BOM 0.5.14" in guide
assert "v0.5.14-fix-version-smokes-no-bom" in guide
assert "nao executa entrega inter-chat" in doc
assert "UTF-8 sem BOM" in doc
print("OK fix_version_smokes_no_bom_0514 0.5.14")
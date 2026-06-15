from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

def version_tuple(value):
    return tuple(int(part) for part in value.split("."))

version_bytes = (ROOT / "VERSION").read_bytes()
assert not version_bytes.startswith(b"\xef\xbb\xbf"), version_bytes
VERSION = version_bytes.decode("utf-8").strip()
assert version_tuple(VERSION) >= version_tuple("0.5.20"), VERSION

manifest = json.loads((ROOT / "extension" / "manifest.json").read_text(encoding="utf-8-sig"))
assert manifest["version"] == VERSION, manifest
assert VERSION in manifest["name"], manifest["name"]

smoke_all = ROOT / "scripts" / "watcher" / "smoke_all.py"
doc = (ROOT / "docs" / "SMOKE_ALL_0520.md").read_text(encoding="utf-8-sig")
guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")

assert smoke_all.exists(), smoke_all
text = smoke_all.read_text(encoding="utf-8-sig")
assert "subprocess.run" in text
assert "smoke_*.py" in text
assert "smoke_all.py" in text
assert "SKIPPED_LEGACY_SMOKES" in text
assert "smoke_composer_submit_guard.py" in text
assert "smoke_rollback_helper.py" in text
assert "OK smoke_all" in text

assert "Smoke all 0.5.20" in doc
assert "nao executa entrega inter-chat" in doc
assert "Smokes legados pulados" in doc
assert "Version alignment 0.5.20" in guide
assert "Smoke all 0.5.20" in guide
assert "v0.5.20-release-process-batch" in guide

print("OK smoke_all_0520 " + VERSION)
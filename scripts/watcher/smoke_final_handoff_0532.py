from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "watcher"))

from final_handoff_summary import build_final_handoff_summary

version_bytes = (ROOT / "VERSION").read_bytes()
assert not version_bytes.startswith(b"\xef\xbb\xbf"), version_bytes
VERSION = version_bytes.decode("utf-8").strip()
assert VERSION == "0.5.32", VERSION

manifest = json.loads((ROOT / "extension" / "manifest.json").read_text(encoding="utf-8-sig"))
assert manifest["version"] == VERSION, manifest
assert VERSION in manifest["name"], manifest["name"]

summary = build_final_handoff_summary()
assert summary["readonly"] is True
assert summary["version"] == VERSION
assert summary["complete"] is True, summary
assert summary["missing_phrases"] == []

handoff = (ROOT / "docs" / "AI_BRIDGE_LOCAL_FINAL_HANDOFF_0532.md").read_text(encoding="utf-8-sig")
doc = (ROOT / "docs" / "FINAL_HANDOFF_0532.md").read_text(encoding="utf-8-sig")
guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")

assert "AI Bridge Local final handoff 0.5.32" in handoff
assert "Nenhuma entrega real inter-chat foi executada" in handoff
assert "Final handoff 0.5.32" in doc
assert "nao executa entrega inter-chat" in doc
assert "Version alignment 0.5.32" in guide
assert "Final safe handoff 0.5.32" in guide
assert "v0.5.32-final-safe-handoff" in guide

print("OK final_handoff_0532 0.5.32")
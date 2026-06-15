from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "watcher"))

from live_interchat_authorization_gate import (
    AUTHORIZATION_PHRASE,
    REQUIRED_PAYLOAD_MARKER,
    evaluate_live_interchat_authorization,
    render_live_interchat_authorization,
)

version_bytes = (ROOT / "VERSION").read_bytes()
assert not version_bytes.startswith(b"\xef\xbb\xbf"), version_bytes
VERSION = version_bytes.decode("utf-8").strip()
assert VERSION == "0.5.33", VERSION

manifest = json.loads((ROOT / "extension" / "manifest.json").read_text(encoding="utf-8-sig"))
assert manifest["version"] == VERSION, manifest
assert VERSION in manifest["name"], manifest["name"]

good = {
    "authorization": AUTHORIZATION_PHRASE,
    "source_chat_id": "source-1",
    "target_chat_id": "target-1",
    "payload": REQUIRED_PAYLOAD_MARKER + " smoke controlado",
    "dry_run_passed": True,
    "preflight_allowed": True,
    "repo_clean": True,
    "manual_operator_present": True,
}

result = evaluate_live_interchat_authorization(good)
assert result["readonly"] is True
assert result["will_send"] is False
assert result["authorized_for_separate_live_runner"] is True
assert result["missing"] == []

bad = dict(good)
bad["authorization"] = "wrong"
bad["payload"] = "sem marcador"
bad_result = evaluate_live_interchat_authorization(bad)
assert bad_result["authorized_for_separate_live_runner"] is False
assert "explicit_authorization_phrase" in bad_result["missing"]
assert "payload_has_live_marker" in bad_result["missing"]
assert bad_result["will_send"] is False

rendered = render_live_interchat_authorization(bad_result)
assert "# Live interchat authorization gate" in rendered
assert "readonly=true" in rendered
assert "will_send=false" in rendered
assert "This gate never sends messages." in rendered

doc = (ROOT / "docs" / "LIVE_INTERCHAT_AUTHORIZATION_GATE_0533.md").read_text(encoding="utf-8-sig")
guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")
assert "Live interchat authorization gate 0.5.33" in doc
assert "nao executa entrega inter-chat" in doc
assert "Version alignment 0.5.33" in guide
assert "Live interchat authorization gate 0.5.33" in guide
assert "v0.5.33-live-interchat-authorization-gate" in guide

print("OK live_interchat_authorization_gate_0533 0.5.33")
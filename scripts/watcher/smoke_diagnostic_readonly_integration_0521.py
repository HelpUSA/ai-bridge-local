from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "watcher"))

from delivery_diagnostic_integration import classify_delivery_event, classify_delivery_events  # noqa: E402

def version_tuple(value):
    return tuple(int(part) for part in value.split("."))

VERSION = (ROOT / "VERSION").read_text(encoding="utf-8-sig").strip()
assert version_tuple(VERSION) >= version_tuple("0.5.21"), VERSION

doc = (ROOT / "docs" / "DIAGNOSTIC_READONLY_INTEGRATION_0521.md").read_text(encoding="utf-8-sig")
guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")

event = {
    "command_id": "cmd-test-001",
    "target_chat_id": "target-test",
    "status": "failed",
    "error": "submit_not_confirmed_composer_still_has_text",
}

result = classify_delivery_event(event)
assert result["readonly"] is True
assert result["diagnostic"]["code"] == "submit_not_confirmed", result
assert result["source"]["command_id"] == "cmd-test-001"
assert result["source"]["target_chat_id"] == "target-test"
assert result["source"]["status"] == "failed"

many = classify_delivery_events([event, {"stderr": "tab not found for target chat"}])
assert len(many) == 2
assert many[1]["diagnostic"]["code"] == "target_tab_not_open"

assert "Diagnostic classifier readonly integration 0.5.21" in doc
assert "Nao executa entrega inter-chat" in doc
assert "Diagnostic classifier readonly integration 0.5.21" in guide

print("OK diagnostic_readonly_integration_0521 " + VERSION)
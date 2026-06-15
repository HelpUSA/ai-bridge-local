from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "watcher"))

from delivery_diagnostic_formatter import format_delivery_diagnostic_result  # noqa: E402
from delivery_diagnostic_integration import classify_delivery_event  # noqa: E402

version_bytes = (ROOT / "VERSION").read_bytes()
assert not version_bytes.startswith(b"\xef\xbb\xbf"), version_bytes
VERSION = version_bytes.decode("utf-8").strip()
assert VERSION == "0.5.23", VERSION

fixtures_path = ROOT / "scripts" / "watcher" / "fixtures" / "delivery_failure_fixtures_0523.json"
fixtures = json.loads(fixtures_path.read_text(encoding="utf-8-sig"))
assert len(fixtures) >= 9

seen_codes = set()
for fixture in fixtures:
    result = classify_delivery_event(fixture["event"])
    expected = fixture["expected_code"]
    actual = result["diagnostic"]["code"]
    assert actual == expected, (fixture["name"], actual, expected)
    rendered = format_delivery_diagnostic_result(result)
    assert "tipo=" + expected in rendered
    assert "readonly=true" in rendered
    seen_codes.add(expected)

required_codes = {
    "submit_not_confirmed",
    "modal_blocking",
    "send_button_disabled",
    "composer_not_found",
    "target_chat_not_registered",
    "target_tab_not_open",
    "delivery_not_acked",
    "inject_timeout",
    "unknown_delivery_failure",
}
assert required_codes.issubset(seen_codes), seen_codes

doc = (ROOT / "docs" / "DELIVERY_FAILURE_FIXTURES_0523.md").read_text(encoding="utf-8-sig")
guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")
assert "Delivery failure fixtures 0.5.23" in doc
assert "nao executam entrega inter-chat" in doc
assert "Version alignment 0.5.23" in guide
assert "Diagnostic readonly batch 0.5.23" in guide
assert "v0.5.23-diagnostic-readonly-batch" in guide

print("OK delivery_failure_fixtures_0523 0.5.23")
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "watcher"))

from delivery_preflight_readonly import (  # noqa: E402
    REQUIRED_CHECKS,
    render_delivery_preflight,
    run_delivery_preflight,
)

def version_tuple(value):
    return tuple(int(part) for part in value.split("."))

VERSION = (ROOT / "VERSION").read_text(encoding="utf-8-sig").strip()
assert version_tuple(VERSION) >= version_tuple("0.5.27"), VERSION

good = {
    "source_chat_id": "source-1",
    "target_chat_id": "target-1",
    "target_registered": True,
    "target_tab_open": True,
    "composer_available": True,
    "composer_empty": True,
    "send_button_enabled": True,
    "blocking_modal": False,
    "payload": "hello dry run",
    "manual_authorization": True,
}

good_result = run_delivery_preflight(good)
assert good_result["readonly"] is True
assert good_result["allowed"] is True
assert good_result["missing"] == []

bad = dict(good)
bad["composer_empty"] = False
bad["manual_authorization"] = False
bad_result = run_delivery_preflight(bad)
assert bad_result["allowed"] is False
assert "composer_empty" in bad_result["missing"]
assert "manual_authorization" in bad_result["missing"]

rendered = render_delivery_preflight(bad_result)
assert "# Delivery preflight readonly" in rendered
assert "readonly=true" in rendered
assert "allowed=false" in rendered

for check in REQUIRED_CHECKS:
    assert check in rendered

doc = (ROOT / "docs" / "DELIVERY_PREFLIGHT_READONLY_0527.md").read_text(encoding="utf-8-sig")
guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")
assert "Delivery preflight readonly 0.5.27" in doc
assert "nao executa entrega inter-chat" in doc
assert "Delivery preflight readonly 0.5.27" in guide

print("OK delivery_preflight_readonly_0527 " + VERSION)
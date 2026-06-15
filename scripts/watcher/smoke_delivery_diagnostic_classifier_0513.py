from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "watcher"))

from delivery_diagnostic_classifier import (  # noqa: E402
    DIAGNOSTIC_CODES,
    classify_delivery_failure,
    format_diagnostic,
)

VERSION = (ROOT / "VERSION").read_text(encoding="utf-8-sig").strip()
GUIDE = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")
DOC_0512 = (ROOT / "docs" / "DELIVERY_DIAGNOSTICS_0512.md").read_text(encoding="utf-8-sig")
DOC_0513 = (ROOT / "docs" / "DELIVERY_DIAGNOSTICS_0513.md").read_text(encoding="utf-8-sig")

def version_tuple(value):
    return tuple(int(part) for part in value.split("."))

assert version_tuple(VERSION) >= version_tuple("0.5.13"), VERSION
assert "Version alignment 0.5.13" in GUIDE
assert "Delivery diagnostic classifier 0.5.13" in GUIDE
assert "v0.5.13-delivery-diagnostic-classifier" in GUIDE
assert "Delivery diagnostic classifier 0.5.13" in DOC_0513

required_codes = {
    "target_chat_not_registered",
    "target_tab_not_open",
    "composer_not_found",
    "modal_blocking",
    "send_button_disabled",
    "inject_timeout",
    "submit_not_confirmed",
    "delivery_not_acked",
    "unknown_delivery_failure",
}
assert required_codes.issubset(set(DIAGNOSTIC_CODES))

cases = {
    "submit_not_confirmed_composer_still_has_text": "submit_not_confirmed",
    "Share/Compartilhar modal blocking detected": "modal_blocking",
    "submit_button_not_found_or_disabled": "send_button_disabled",
    "composer not found on target page": "composer_not_found",
    "target_chat_not_registered in local registry": "target_chat_not_registered",
    "tab not found for target chat": "target_tab_not_open",
    "delivery_not_acked after delivering state": "delivery_not_acked",
    "inject_timeout waiting for content script": "inject_timeout",
    "totally new error": "unknown_delivery_failure",
}

for text, expected in cases.items():
    actual = classify_delivery_failure(text)
    assert actual.code == expected, (text, actual, expected)
    rendered = format_diagnostic(text)
    assert "tipo=" + expected in rendered
    assert "correcao=" in rendered

for code in required_codes - {"delivery_not_acked", "unknown_delivery_failure"}:
    assert code in DOC_0512, code

assert "nao executa entrega inter-chat" in DOC_0512
print("OK delivery_diagnostic_classifier_0513 " + VERSION)
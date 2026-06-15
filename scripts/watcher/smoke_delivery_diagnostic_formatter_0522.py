from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "watcher"))

from delivery_diagnostic_integration import classify_delivery_event  # noqa: E402
from delivery_diagnostic_formatter import (  # noqa: E402
    ORDERED_FIELDS,
    format_delivery_diagnostic_result,
    format_delivery_diagnostic_results,
)

def version_tuple(value):
    return tuple(int(part) for part in value.split("."))

VERSION = (ROOT / "VERSION").read_text(encoding="utf-8-sig").strip()
assert version_tuple(VERSION) >= version_tuple("0.5.22"), VERSION

doc = (ROOT / "docs" / "DELIVERY_DIAGNOSTIC_FORMATTER_0522.md").read_text(encoding="utf-8-sig")
guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")

result = classify_delivery_event({
    "command_id": "cmd-format-001",
    "target_chat_id": "target-format",
    "status": "failed",
    "stderr": "tab not found for target chat",
})

rendered = format_delivery_diagnostic_result(result)
for field in ORDERED_FIELDS:
    assert field + "=" in rendered, field

assert "tipo=target_tab_not_open" in rendered
assert "readonly=true" in rendered
assert "command_id=cmd-format-001" in rendered

many = format_delivery_diagnostic_results([result, result])
assert "diagnostic_index=1" in many
assert "diagnostic_index=2" in many

assert "Delivery diagnostic formatter 0.5.22" in doc
assert "nao executa entrega inter-chat" in doc
assert "Delivery diagnostic formatter 0.5.22" in guide

print("OK delivery_diagnostic_formatter_0522 " + VERSION)
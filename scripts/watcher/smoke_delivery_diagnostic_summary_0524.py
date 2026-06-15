from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "watcher"))

from delivery_diagnostic_summary import (  # noqa: E402
    render_delivery_diagnostic_summary,
    summarize_delivery_diagnostics,
)

def version_tuple(value):
    return tuple(int(part) for part in value.split("."))

VERSION = (ROOT / "VERSION").read_text(encoding="utf-8-sig").strip()
assert version_tuple(VERSION) >= version_tuple("0.5.24"), VERSION

events = [
    {"status": "failed", "error": "submit_not_confirmed_composer_still_has_text"},
    {"status": "failed", "stderr": "tab not found for target chat"},
    {"status": "delivering", "delivery_result": "delivery_not_acked after delivering state"},
]

summary = summarize_delivery_diagnostics(events)
assert summary["readonly"] is True
assert summary["total"] == 3
assert summary["by_code"]["submit_not_confirmed"] == 1
assert summary["by_code"]["target_tab_not_open"] == 1
assert summary["by_code"]["delivery_not_acked"] == 1
assert summary["by_status"]["failed"] == 2
assert summary["by_status"]["delivering"] == 1

rendered = render_delivery_diagnostic_summary(summary)
assert "# Delivery diagnostic summary" in rendered
assert "readonly=true" in rendered
assert "- submit_not_confirmed: 1" in rendered

doc = (ROOT / "docs" / "DELIVERY_DIAGNOSTIC_SUMMARY_0524.md").read_text(encoding="utf-8-sig")
guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")
assert "Delivery diagnostic summary 0.5.24" in doc
assert "Nao executa entrega inter-chat" in doc
assert "Delivery diagnostic summary 0.5.24" in guide

print("OK delivery_diagnostic_summary_0524 " + VERSION)
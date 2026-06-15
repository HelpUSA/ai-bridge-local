from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "watcher"))

from final_stabilization_status import (
    build_final_stabilization_status,
    render_final_stabilization_status,
)

def version_tuple(value):
    return tuple(int(part) for part in value.split("."))

VERSION = (ROOT / "VERSION").read_text(encoding="utf-8-sig").strip()
assert version_tuple(VERSION) >= version_tuple("0.5.30"), VERSION

status = build_final_stabilization_status()
assert status["readonly"] is True
assert status["utf8_no_bom"] is True
assert status["missing_required_files"] == []
assert status["safe_ready"] is True
assert status["real_inter_chat_delivery"] is False

rendered = render_final_stabilization_status(status)
assert "# Final stabilization status" in rendered
assert "readonly=true" in rendered
assert "safe_ready=true" in rendered
assert "real_inter_chat_delivery=false" in rendered

doc = (ROOT / "docs" / "FINAL_STABILIZATION_0530.md").read_text(encoding="utf-8-sig")
guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")
assert "Final stabilization 0.5.30" in doc
assert "nao executa entrega inter-chat" in doc
assert "Final stabilization 0.5.30" in guide

print("OK final_stabilization_0530 " + VERSION)
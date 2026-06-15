from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "watcher"))

from final_safe_audit import render_final_safe_audit, run_final_safe_audit

def version_tuple(value):
    return tuple(int(part) for part in value.split("."))

VERSION = (ROOT / "VERSION").read_text(encoding="utf-8-sig").strip()
assert version_tuple(VERSION) >= version_tuple("0.5.31"), VERSION

audit = run_final_safe_audit()
assert audit["readonly"] is True
assert audit["passed"] is True, audit
assert audit["issues"] == []

rendered = render_final_safe_audit(audit)
assert "# Final safe audit" in rendered
assert "readonly=true" in rendered
assert "passed=true" in rendered
assert "- none" in rendered

doc = (ROOT / "docs" / "FINAL_AUDIT_0531.md").read_text(encoding="utf-8-sig")
guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")
assert "Final audit 0.5.31" in doc
assert "nao executa entrega inter-chat" in doc
assert "Final audit 0.5.31" in guide

print("OK final_audit_0531 " + VERSION)
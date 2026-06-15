from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "watcher"))

from delivery_diagnostic_summary import summarize_delivery_diagnostics  # noqa: E402
from operational_report_generator import build_operational_report  # noqa: E402
from queue_worker_health import build_queue_worker_health_snapshot  # noqa: E402

version_bytes = (ROOT / "VERSION").read_bytes()
assert not version_bytes.startswith(b"\xef\xbb\xbf"), version_bytes
VERSION = version_bytes.decode("utf-8").strip()
assert VERSION == "0.5.26", VERSION

manifest = json.loads((ROOT / "extension" / "manifest.json").read_text(encoding="utf-8-sig"))
assert manifest["version"] == VERSION, manifest
assert VERSION in manifest["name"], manifest["name"]

diagnostic_summary = summarize_delivery_diagnostics([
    {"status": "failed", "error": "submit_not_confirmed_composer_still_has_text"},
])
queue_health = build_queue_worker_health_snapshot({
    "commands": [{"status": "acked"}],
    "workers": [{"id": "w1", "state": "running"}],
    "locks": [],
})

report = build_operational_report({
    "version": VERSION,
    "tag": "v0.5.26-observability-readonly-batch",
    "commit": "pending",
    "diagnostic_summary": diagnostic_summary,
    "queue_health": queue_health,
    "validations": ["smoke_all.py", "smoke_docs.py"],
    "risks": ["manual review required before real delivery"],
    "next_steps": ["preflight readonly before guarded delivery"],
})

assert "# AI Bridge Local operational report" in report
assert "version=0.5.26" in report
assert "tag=v0.5.26-observability-readonly-batch" in report
assert "readonly=true" in report
assert "## Diagnostic summary" in report
assert "## Queue worker health" in report
assert "Does not run inter-chat delivery." in report

doc = (ROOT / "docs" / "OPERATIONAL_REPORT_GENERATOR_0526.md").read_text(encoding="utf-8-sig")
guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")
assert "Operational report generator 0.5.26" in doc
assert "Nao executa entrega inter-chat" in doc
assert "Version alignment 0.5.26" in guide
assert "Observability readonly batch 0.5.26" in guide
assert "v0.5.26-observability-readonly-batch" in guide

print("OK operational_report_generator_0526 0.5.26")
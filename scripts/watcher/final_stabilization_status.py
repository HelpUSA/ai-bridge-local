from __future__ import annotations

from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

def build_final_stabilization_status() -> dict[str, Any]:
    version_bytes = (ROOT / "VERSION").read_bytes()
    version = version_bytes.decode("utf-8").strip()

    required_files = [
        "VERSION",
        "extension/manifest.json",
        "docs/AI_BRIDGE_LOCAL_GUIDE.md",
        "scripts/watcher/smoke_all.py",
        "scripts/watcher/dry_run_delivery_plan.py",
        "scripts/watcher/delivery_preflight_readonly.py",
        "scripts/watcher/operational_report_generator.py",
        "scripts/release/run_safe_release.ps1",
    ]

    missing = [path for path in required_files if not (ROOT / path).exists()]

    return {
        "readonly": True,
        "version": version,
        "utf8_no_bom": not version_bytes.startswith(b"\xef\xbb\xbf"),
        "required_files_total": len(required_files),
        "missing_required_files": missing,
        "safe_ready": not missing and not version_bytes.startswith(b"\xef\xbb\xbf"),
        "real_inter_chat_delivery": False,
    }

def render_final_stabilization_status(status: dict[str, Any]) -> str:
    lines = [
        "# Final stabilization status",
        "",
        "readonly=" + str(bool(status.get("readonly", False))).lower(),
        "version=" + str(status.get("version", "")),
        "utf8_no_bom=" + str(bool(status.get("utf8_no_bom", False))).lower(),
        "required_files_total=" + str(status.get("required_files_total", 0)),
        "safe_ready=" + str(bool(status.get("safe_ready", False))).lower(),
        "real_inter_chat_delivery=" + str(bool(status.get("real_inter_chat_delivery", True))).lower(),
        "",
        "## Missing required files",
    ]

    missing = list(status.get("missing_required_files", []) or [])
    if missing:
        for item in missing:
            lines.append("- " + str(item))
    else:
        lines.append("- none")

    return "\n".join(lines) + "\n"
from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]

def run_final_safe_audit() -> dict[str, object]:
    version_bytes = (ROOT / "VERSION").read_bytes()
    version = version_bytes.decode("utf-8").strip()
    manifest = json.loads((ROOT / "extension" / "manifest.json").read_text(encoding="utf-8-sig"))

    issues: list[str] = []

    if version_bytes.startswith(b"\xef\xbb\xbf"):
        issues.append("version_has_bom")

    if manifest.get("version") != version:
        issues.append("manifest_version_mismatch")

    if version not in str(manifest.get("name", "")):
        issues.append("manifest_name_missing_version")

    guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")
    if "Version alignment " + version not in guide:
        issues.append("guide_missing_current_version_alignment")

    ps1_files = sorted((ROOT / "scripts").rglob("*.ps1"))
    bad_token = "ex" + "it"
    for path in ps1_files:
        text = path.read_text(encoding="utf-8-sig")
        for line_number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if re.match(r"(?i)^" + bad_token + r"(\s|$)", stripped):
                issues.append("shell_close_token:" + path.relative_to(ROOT).as_posix() + ":" + str(line_number))

    required_tags = [
        "v0.5.20-release-process-batch",
        "v0.5.23-diagnostic-readonly-batch",
        "v0.5.26-observability-readonly-batch",
        "v0.5.28-preflight-dry-run-batch",
    ]
    for tag in required_tags:
        if tag not in guide:
            issues.append("guide_missing_tag:" + tag)

    return {
        "readonly": True,
        "version": version,
        "issues": issues,
        "passed": len(issues) == 0,
        "checked_ps1_files": len(ps1_files),
    }

def render_final_safe_audit(audit: dict[str, object]) -> str:
    lines = [
        "# Final safe audit",
        "",
        "readonly=" + str(bool(audit.get("readonly", False))).lower(),
        "version=" + str(audit.get("version", "")),
        "passed=" + str(bool(audit.get("passed", False))).lower(),
        "checked_ps1_files=" + str(audit.get("checked_ps1_files", 0)),
        "",
        "## Issues",
    ]

    issues = list(audit.get("issues", []) or [])
    if issues:
        for issue in issues:
            lines.append("- " + str(issue))
    else:
        lines.append("- none")

    return "\n".join(lines) + "\n"
from __future__ import annotations

from typing import Any, Mapping

AUTHORIZATION_PHRASE = "I_AUTHORIZE_REAL_INTERCHAT_SMOKE"
REQUIRED_PAYLOAD_MARKER = "[AI_BRIDGE_LIVE_SMOKE]"

def evaluate_live_interchat_authorization(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    source_chat_id = str(snapshot.get("source_chat_id", "")).strip()
    target_chat_id = str(snapshot.get("target_chat_id", "")).strip()
    payload = str(snapshot.get("payload", "")).strip()
    authorization = str(snapshot.get("authorization", "")).strip()

    checks = {
        "explicit_authorization_phrase": authorization == AUTHORIZATION_PHRASE,
        "source_chat_id_present": bool(source_chat_id),
        "target_chat_id_present": bool(target_chat_id),
        "source_target_distinct": bool(source_chat_id and target_chat_id and source_chat_id != target_chat_id),
        "payload_present": bool(payload),
        "payload_has_live_marker": REQUIRED_PAYLOAD_MARKER in payload,
        "dry_run_passed": bool(snapshot.get("dry_run_passed", False)),
        "preflight_allowed": bool(snapshot.get("preflight_allowed", False)),
        "repo_clean": bool(snapshot.get("repo_clean", False)),
        "manual_operator_present": bool(snapshot.get("manual_operator_present", False)),
    }

    missing = [name for name, value in checks.items() if not value]

    return {
        "readonly": True,
        "will_send": False,
        "authorized_for_separate_live_runner": len(missing) == 0,
        "checks": checks,
        "missing": missing,
        "source_chat_id": source_chat_id,
        "target_chat_id": target_chat_id,
        "payload_preview": payload[:120],
        "required_authorization_phrase": AUTHORIZATION_PHRASE,
        "required_payload_marker": REQUIRED_PAYLOAD_MARKER,
        "reason": "authorization gate only; this module never sends messages",
    }

def render_live_interchat_authorization(result: Mapping[str, Any]) -> str:
    lines = [
        "# Live interchat authorization gate",
        "",
        "readonly=" + str(bool(result.get("readonly", False))).lower(),
        "will_send=" + str(bool(result.get("will_send", True))).lower(),
        "authorized_for_separate_live_runner=" + str(bool(result.get("authorized_for_separate_live_runner", False))).lower(),
        "source_chat_id=" + str(result.get("source_chat_id", "")),
        "target_chat_id=" + str(result.get("target_chat_id", "")),
        "",
        "## Checks",
    ]

    for name, value in dict(result.get("checks", {})).items():
        lines.append("- " + str(name) + ": " + str(bool(value)).lower())

    lines.append("")
    lines.append("## Missing")
    missing = list(result.get("missing", []) or [])
    if missing:
        for item in missing:
            lines.append("- " + str(item))
    else:
        lines.append("- none")

    lines.append("")
    lines.append("## Safety")
    lines.append("- This gate never sends messages.")
    lines.append("- This gate never clicks UI.")
    lines.append("- This gate only authorizes a separate live runner.")

    return "\n".join(lines) + "\n"
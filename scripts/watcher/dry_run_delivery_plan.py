# -*- coding: utf-8 -*-
"""Readonly dry-run delivery plan builder."""

from __future__ import annotations

from typing import Any, Mapping

from delivery_preflight_readonly import render_delivery_preflight, run_delivery_preflight


def build_dry_run_delivery_plan(request: Mapping[str, Any]) -> dict[str, Any]:
    preflight = run_delivery_preflight(request)

    payload = str(request.get("payload", ""))
    command_id = str(request.get("command_id", ""))
    target_chat_id = str(request.get("target_chat_id", ""))

    actions = [
        "validate_preflight",
        "prepare_payload",
        "confirm_target_context",
        "require_manual_authorization",
    ]

    if preflight.get("allowed"):
        actions.append("ready_for_separate_guarded_delivery")
    else:
        actions.append("stop_before_delivery")

    return {
        "readonly": True,
        "will_send": False,
        "command_id": command_id,
        "target_chat_id": target_chat_id,
        "payload_preview": payload[:120],
        "payload_length": len(payload),
        "preflight": preflight,
        "actions": actions,
        "risk": "low_readonly" if preflight.get("allowed") else "blocked_by_preflight",
    }


def render_dry_run_delivery_plan(plan: Mapping[str, Any]) -> str:
    lines = [
        "# Dry-run delivery plan",
        "",
        "readonly=" + str(bool(plan.get("readonly", False))).lower(),
        "will_send=" + str(bool(plan.get("will_send", False))).lower(),
        "command_id=" + str(plan.get("command_id", "")),
        "target_chat_id=" + str(plan.get("target_chat_id", "")),
        "payload_length=" + str(plan.get("payload_length", 0)),
        "risk=" + str(plan.get("risk", "")),
        "",
        "## Actions",
    ]

    for action in list(plan.get("actions", []) or []):
        lines.append("- " + str(action))

    lines.append("")
    lines.append("## Preflight")
    lines.append(render_delivery_preflight(plan.get("preflight", {}) or {}).strip())

    lines.append("")
    lines.append("## Safety")
    lines.append("- Dry run only.")
    lines.append("- Does not send messages.")
    lines.append("- Does not mutate queues.")
    lines.append("- Does not click UI.")

    return "\n".join(lines) + "\n"


__all__ = [
    "build_dry_run_delivery_plan",
    "render_dry_run_delivery_plan",
]
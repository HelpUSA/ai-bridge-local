# -*- coding: utf-8 -*-
"""Readonly preflight checks before any guarded delivery."""

from __future__ import annotations

from typing import Any, Mapping


REQUIRED_CHECKS = (
    "target_chat_id",
    "target_registered",
    "target_tab_open",
    "composer_available",
    "composer_empty",
    "send_button_enabled",
    "no_blocking_modal",
    "source_target_distinct",
    "payload_present",
    "manual_authorization",
)


def run_delivery_preflight(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    checks = {}

    source_chat_id = str(snapshot.get("source_chat_id", "")).strip()
    target_chat_id = str(snapshot.get("target_chat_id", "")).strip()
    payload = str(snapshot.get("payload", "")).strip()

    checks["target_chat_id"] = bool(target_chat_id)
    checks["target_registered"] = bool(snapshot.get("target_registered", False))
    checks["target_tab_open"] = bool(snapshot.get("target_tab_open", False))
    checks["composer_available"] = bool(snapshot.get("composer_available", False))
    checks["composer_empty"] = bool(snapshot.get("composer_empty", False))
    checks["send_button_enabled"] = bool(snapshot.get("send_button_enabled", False))
    checks["no_blocking_modal"] = not bool(snapshot.get("blocking_modal", False))
    checks["source_target_distinct"] = bool(source_chat_id and target_chat_id and source_chat_id != target_chat_id)
    checks["payload_present"] = bool(payload)
    checks["manual_authorization"] = bool(snapshot.get("manual_authorization", False))

    missing = [name for name in REQUIRED_CHECKS if not checks.get(name, False)]

    return {
        "readonly": True,
        "allowed": len(missing) == 0,
        "checks": checks,
        "missing": missing,
        "source_chat_id": source_chat_id,
        "target_chat_id": target_chat_id,
    }


def render_delivery_preflight(result: Mapping[str, Any]) -> str:
    lines = [
        "# Delivery preflight readonly",
        "",
        "readonly=" + str(bool(result.get("readonly", False))).lower(),
        "allowed=" + str(bool(result.get("allowed", False))).lower(),
        "source_chat_id=" + str(result.get("source_chat_id", "")),
        "target_chat_id=" + str(result.get("target_chat_id", "")),
        "",
        "## Checks",
    ]

    for name in REQUIRED_CHECKS:
        value = dict(result.get("checks", {})).get(name, False)
        lines.append("- " + name + ": " + str(bool(value)).lower())

    lines.append("")
    lines.append("## Missing")
    missing = list(result.get("missing", []) or [])
    if missing:
        for name in missing:
            lines.append("- " + str(name))
    else:
        lines.append("- none")

    return "\n".join(lines) + "\n"


__all__ = [
    "REQUIRED_CHECKS",
    "run_delivery_preflight",
    "render_delivery_preflight",
]
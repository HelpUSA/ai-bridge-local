# -*- coding: utf-8 -*-
"""Readonly operational report generator."""

from __future__ import annotations

from typing import Any, Mapping

from delivery_diagnostic_summary import render_delivery_diagnostic_summary
from queue_worker_health import render_queue_worker_health


def build_operational_report(data: Mapping[str, Any]) -> str:
    version = str(data.get("version", ""))
    tag = str(data.get("tag", ""))
    commit = str(data.get("commit", ""))
    diagnostic_summary = data.get("diagnostic_summary", {}) or {}
    queue_health = data.get("queue_health", {}) or {}
    validations = list(data.get("validations", []) or [])
    risks = list(data.get("risks", []) or [])
    next_steps = list(data.get("next_steps", []) or [])

    lines = [
        "# AI Bridge Local operational report",
        "",
        "version=" + version,
        "tag=" + tag,
        "commit=" + commit,
        "readonly=true",
        "",
        "## Validations",
    ]

    if validations:
        for item in validations:
            lines.append("- " + str(item))
    else:
        lines.append("- none")

    lines.append("")
    lines.append("## Diagnostic summary")
    lines.append(render_delivery_diagnostic_summary(diagnostic_summary).strip())

    lines.append("")
    lines.append("## Queue worker health")
    lines.append(render_queue_worker_health(queue_health).strip())

    lines.append("")
    lines.append("## Risks")
    if risks:
        for item in risks:
            lines.append("- " + str(item))
    else:
        lines.append("- none")

    lines.append("")
    lines.append("## Next steps")
    if next_steps:
        for item in next_steps:
            lines.append("- " + str(item))
    else:
        lines.append("- none")

    lines.append("")
    lines.append("## Safety")
    lines.append("- Does not send messages.")
    lines.append("- Does not mutate queues.")
    lines.append("- Does not run inter-chat delivery.")

    return "\n".join(lines) + "\n"


__all__ = [
    "build_operational_report",
]
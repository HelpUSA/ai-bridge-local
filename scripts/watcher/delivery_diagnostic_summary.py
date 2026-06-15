# -*- coding: utf-8 -*-
"""Readonly local diagnostic summary helpers."""

from __future__ import annotations

from collections import Counter
from typing import Any, Mapping

from delivery_diagnostic_integration import classify_delivery_events


def summarize_delivery_diagnostics(events: list[Mapping[str, Any]]) -> dict[str, Any]:
    results = classify_delivery_events(events)
    by_code = Counter(str(item["diagnostic"].get("code", "")) for item in results)
    by_status = Counter(str(item["source"].get("status", "")) for item in results)

    return {
        "readonly": True,
        "total": len(results),
        "by_code": dict(sorted(by_code.items())),
        "by_status": dict(sorted(by_status.items())),
        "results": results,
    }


def render_delivery_diagnostic_summary(summary: Mapping[str, Any]) -> str:
    lines = [
        "# Delivery diagnostic summary",
        "",
        "readonly=" + str(bool(summary.get("readonly", False))).lower(),
        "total=" + str(summary.get("total", 0)),
        "",
        "## By code",
    ]

    for code, count in dict(summary.get("by_code", {})).items():
        lines.append("- " + str(code) + ": " + str(count))

    lines.append("")
    lines.append("## By status")
    for status, count in dict(summary.get("by_status", {})).items():
        lines.append("- " + str(status) + ": " + str(count))

    return "\n".join(lines) + "\n"


__all__ = [
    "summarize_delivery_diagnostics",
    "render_delivery_diagnostic_summary",
]
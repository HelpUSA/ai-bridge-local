# -*- coding: utf-8 -*-
"""Stable readonly formatting for delivery diagnostics."""

from __future__ import annotations

from typing import Any, Mapping


ORDERED_FIELDS = (
    "tipo",
    "confianca",
    "resumo",
    "correcao",
    "command_id",
    "target_chat_id",
    "status",
    "readonly",
)


def format_delivery_diagnostic_result(result: Mapping[str, Any]) -> str:
    diagnostic = result.get("diagnostic", {}) or {}
    source = result.get("source", {}) or {}

    fields = {
        "tipo": str(diagnostic.get("code", "")),
        "confianca": str(diagnostic.get("confidence", "")),
        "resumo": str(diagnostic.get("summary", "")),
        "correcao": str(diagnostic.get("next_action", "")),
        "command_id": str(source.get("command_id", "")),
        "target_chat_id": str(source.get("target_chat_id", "")),
        "status": str(source.get("status", "")),
        "readonly": str(bool(result.get("readonly", False))).lower(),
    }

    return "\n".join(field + "=" + fields[field] for field in ORDERED_FIELDS)


def format_delivery_diagnostic_results(results: list[Mapping[str, Any]]) -> str:
    blocks = []
    for index, result in enumerate(results, start=1):
        blocks.append("diagnostic_index=" + str(index) + "\n" + format_delivery_diagnostic_result(result))
    return "\n\n".join(blocks)


__all__ = [
    "ORDERED_FIELDS",
    "format_delivery_diagnostic_result",
    "format_delivery_diagnostic_results",
]
# -*- coding: utf-8 -*-
"""Readonly integration helpers for delivery diagnostics.

This module does not send messages, mutate queues, click UI, or run browser
delivery. It only adapts existing error/result text into diagnostic objects.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Mapping

from delivery_diagnostic_classifier import classify_delivery_failure


def _pick_first_text(event: Mapping[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = event.get(key)
        if value is not None and str(value).strip():
            return str(value)
    return ""


def classify_delivery_event(event: Mapping[str, Any]) -> dict[str, Any]:
    """Classify an existing delivery event/result without side effects."""

    text = _pick_first_text(
        event,
        (
            "error",
            "erro",
            "stderr",
            "stdout",
            "message",
            "observacao",
            "delivery_result",
            "status_text",
        ),
    )

    diagnostic = classify_delivery_failure(text)

    result = {
        "diagnostic": asdict(diagnostic),
        "source": {
            "command_id": str(event.get("command_id", "")),
            "target_chat_id": str(event.get("target_chat_id", "")),
            "status": str(event.get("status", "")),
            "raw_text": text,
        },
        "readonly": True,
    }

    return result


def classify_delivery_events(events: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [classify_delivery_event(event) for event in events]


__all__ = [
    "classify_delivery_event",
    "classify_delivery_events",
]
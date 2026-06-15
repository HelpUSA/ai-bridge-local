# -*- coding: utf-8 -*-
"""Readonly queue and worker health snapshot helpers."""

from __future__ import annotations

from collections import Counter
from typing import Any, Mapping


def build_queue_worker_health_snapshot(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    commands = list(snapshot.get("commands", []) or [])
    workers = list(snapshot.get("workers", []) or [])
    locks = list(snapshot.get("locks", []) or [])

    by_status = Counter(str(item.get("status", "")) for item in commands)
    active_workers = [
        worker for worker in workers
        if str(worker.get("state", "")).lower() in {"running", "active", "delivering"}
    ]

    duplicate_active_workers = max(0, len(active_workers) - 1)

    stale_locks = [
        lock for lock in locks
        if str(lock.get("state", "")).lower() in {"stale", "expired", "orphaned"}
    ]

    warnings = []
    if duplicate_active_workers:
        warnings.append("duplicate_active_workers")
    if stale_locks:
        warnings.append("stale_locks_present")
    if by_status.get("failed", 0):
        warnings.append("failed_commands_present")
    if by_status.get("queued", 0) and not active_workers:
        warnings.append("queued_without_active_worker")

    return {
        "readonly": True,
        "command_total": len(commands),
        "by_status": dict(sorted(by_status.items())),
        "worker_total": len(workers),
        "active_worker_count": len(active_workers),
        "duplicate_active_workers": duplicate_active_workers,
        "stale_lock_count": len(stale_locks),
        "warnings": warnings,
        "healthy": len(warnings) == 0,
    }


def render_queue_worker_health(snapshot: Mapping[str, Any]) -> str:
    lines = [
        "# Queue worker health",
        "",
        "readonly=" + str(bool(snapshot.get("readonly", False))).lower(),
        "healthy=" + str(bool(snapshot.get("healthy", False))).lower(),
        "command_total=" + str(snapshot.get("command_total", 0)),
        "worker_total=" + str(snapshot.get("worker_total", 0)),
        "active_worker_count=" + str(snapshot.get("active_worker_count", 0)),
        "duplicate_active_workers=" + str(snapshot.get("duplicate_active_workers", 0)),
        "stale_lock_count=" + str(snapshot.get("stale_lock_count", 0)),
        "",
        "## Warnings",
    ]

    warnings = list(snapshot.get("warnings", []) or [])
    if warnings:
        for warning in warnings:
            lines.append("- " + str(warning))
    else:
        lines.append("- none")

    lines.append("")
    lines.append("## Commands by status")
    for status, count in dict(snapshot.get("by_status", {})).items():
        lines.append("- " + str(status) + ": " + str(count))

    return "\n".join(lines) + "\n"


__all__ = [
    "build_queue_worker_health_snapshot",
    "render_queue_worker_health",
]
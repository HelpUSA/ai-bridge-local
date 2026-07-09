#!/usr/bin/env python3
"""Smoke test for Control Center diagnostics endpoint integration."""

from __future__ import annotations

from pathlib import Path


def main() -> int:
    print("SMOKE_CONTROL_CENTER_DIAGNOSTICS_INTEGRATION_START", flush=True)
    text = Path("app_windows/control_center_app.py").read_text(encoding="utf-8")
    assert 'DIAGNOSTICS_URL = "http://127.0.0.1:8766/control/diagnostics"' in text
    assert "for endpoint in [DIAGNOSTICS_URL, URL]:" in text
    assert 'data["_control_center_endpoint"] = endpoint' in text
    assert 'data["_control_center_fallback"] = "control/status"' in text
    assert 'data.get("command_status", {}) or data.get("queue", {})' in text
    assert "Modo gateway-first: ativo" in text
    assert "Diagnosticos do gateway" in text
    assert "Targets ativos" in text
    print("SMOKE_CONTROL_CENTER_DIAGNOSTICS_INTEGRATION_OK", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

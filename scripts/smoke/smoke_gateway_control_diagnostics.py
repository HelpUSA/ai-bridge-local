#!/usr/bin/env python3
# Smoke test for gateway-first control diagnostics.

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path
import sys


def load_gateway_module():
    repository = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    repository_text = str(
        repository
    )

    inserted = (
        repository_text
        not in sys.path
    )

    if inserted:
        sys.path.insert(
            0,
            repository_text,
        )

    try:
        spec = (
            importlib.util.spec_from_file_location(
                "gateway_local_smoke",
                repository
                / "gateway_local.py",
            )
        )

        if (
            spec is None
            or spec.loader is None
        ):
            raise RuntimeError(
                "could not load gateway_local.py"
            )

        module = (
            importlib.util.module_from_spec(
                spec
            )
        )

        spec.loader.exec_module(
            module
        )

        return module

    finally:
        if inserted:
            try:
                sys.path.remove(
                    repository_text
                )
            except ValueError:
                pass


def main() -> int:
    print("SMOKE_GATEWAY_CONTROL_DIAGNOSTICS_START", flush=True)
    gateway = load_gateway_module()
    with tempfile.TemporaryDirectory() as tmp:
        gateway.DB_PATH = str(Path(tmp) / "queue_local_smoke.db")
        gateway.init_db()
        data = gateway.fetch_gateway_diagnostics()

    assert data["ok"] is True
    assert data["service"] == "ai-bridge-local"
    assert data["gateway_first"] is True
    assert data["compatibility"] == "0.5.86-envelope-compatible"
    assert data["control_plane"]["owns_validation"] is True
    assert data["control_plane"]["extension_role"] == "thin transport"
    assert "queue" in data
    assert "browser" in data
    assert "diagnostics" in data
    assert isinstance(data["diagnostics"]["recommended_next_checks"], list)
    print("SMOKE_GATEWAY_CONTROL_DIAGNOSTICS_OK", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

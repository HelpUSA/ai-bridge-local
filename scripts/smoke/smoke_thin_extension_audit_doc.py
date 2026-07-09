#!/usr/bin/env python3
"""Smoke test for the thin-extension gateway-first audit doc."""

from pathlib import Path


def main() -> int:
    print("SMOKE_THIN_EXTENSION_AUDIT_DOC_START", flush=True)
    path = Path("docs/status/2026-07-09-ai-bridge-local-0.5.85-thin-extension-audit.md")
    text = path.read_text(encoding="utf-8")
    assert "thin-extension gateway-first audit" in text
    assert "Gateway-first reading" in text
    assert "This audit does not change extension behavior." in text
    print("SMOKE_THIN_EXTENSION_AUDIT_DOC_OK", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

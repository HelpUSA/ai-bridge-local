#!/usr/bin/env python3
from pathlib import Path

def check(path, markers):
    text = Path(path).read_text(encoding="utf-8")
    for marker in markers:
        assert marker in text, f"{marker!r} missing from {path}"

def main():
    print("SMOKE_GATEWAY_FIRST_DOCS_CURRENT_STATE_START", flush=True)
    check("docs/status/2026-07-10-ai-bridge-local-0.5.85-gateway-first-current-state.md", ["gateway-first current state", "DIRECT_INTERCHAT_ENABLED", "8e7c3d8", "Remaining risks"])
    check("docs/roadmap/ai-bridge-local-gateway-first-roadmap.md", ["Route-classifier gateway-first enforcement", "Gateway route-decision service", "Release checklist"])
    check("docs/how-to/gateway-first-control-plane-operations.md", ["Operating model", "Direct interchat policy", "Safe patch pattern"])
    print("SMOKE_GATEWAY_FIRST_DOCS_CURRENT_STATE_OK", flush=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

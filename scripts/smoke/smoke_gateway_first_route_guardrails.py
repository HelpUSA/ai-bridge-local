#!/usr/bin/env python3
from pathlib import Path


def main() -> int:
    print("SMOKE_GATEWAY_FIRST_ROUTE_GUARDRAILS_START", flush=True)
    text = Path("extension/background.js").read_text(encoding="utf-8")

    assert "globalThis.aiBridgeClassifyRouteSafe" in text
    assert "function mustUseGateway(cmd)" in text
    assert "const DIRECT_INTERCHAT_ENABLED = false;" in text
    assert "return !DIRECT_INTERCHAT_ENABLED;" in text

    route_lock_pos = text.find("AI Bridge Local 0.5.85 gateway-first route lock")
    classify_pos = text.find("globalThis.aiBridgeClassifyRouteSafe")
    assert classify_pos >= 0
    assert route_lock_pos > classify_pos

    route_lock = text[route_lock_pos:]
    assert 'route === "direct_interchat"' in route_lock
    assert 'return "local_gateway";' in route_lock
    assert "DIRECT_INTERCHAT_DISABLED_REASON" in route_lock
    assert "aiBridgeGatewayFirstLastBlockedRoute" in route_lock

    print("SMOKE_GATEWAY_FIRST_ROUTE_GUARDRAILS_OK", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

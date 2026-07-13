#!/usr/bin/env python3
from pathlib import Path


def main() -> int:
    print("SMOKE_GATEWAY_FIRST_DIRECT_INTERCHAT_DISABLED_START", flush=True)
    text = Path("extension/background.js").read_text(encoding="utf-8")

    required = [
        "const DIRECT_INTERCHAT_ENABLED = false;",
        "const DIRECT_INTERCHAT_DISABLED_REASON",
        "return !DIRECT_INTERCHAT_ENABLED;",
        "DIRECT_INTERCHAT_ALLOW_GATEWAY_FALLBACK = true;",
        "AI Bridge Local 0.5.85 gateway-first route lock",
        "aiBridgeClassifyRouteSafeGatewayFirstBase",
        "aiBridgeGatewayFirstLastBlockedRoute",
        'blocked_route: "direct_interchat"',
        'route: "local_gateway"',
    ]

    for marker in required:
        assert marker in text, marker

    assert "const DIRECT_INTERCHAT_ENABLED = true;" not in text
    print("SMOKE_GATEWAY_FIRST_DIRECT_INTERCHAT_DISABLED_OK", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

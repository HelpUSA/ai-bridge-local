#!/usr/bin/env python3
# Guard active extension dispatchers against direct-interchat route ownership.

from pathlib import Path


def between(source: str, start: str, end: str) -> str:
    before, marker, tail = source.partition(start)
    assert marker, start
    body, marker, _ = tail.partition(end)
    assert marker, end
    return body


def main() -> int:
    print("SMOKE_EXTENSION_GATEWAY_ONLY_DISPATCH_START", flush=True)
    source = Path("extension/background.js").read_text(encoding="utf-8")

    classifier = between(
        source,
        "/* AIBRIDGE_ROUTE_CLASSIFIER_LOAD_START */",
        "/* AIBRIDGE_ROUTE_CLASSIFIER_LOAD_END */",
    )
    assert 'return "local_gateway";' in classifier
    assert "route_classifier.js" not in classifier
    assert "direct_interchat" not in classifier

    route_bridge = between(
        source,
        "async function routeBridgeCommand(cmd, sourceLabel) {",
        "/* AIBRIDGE_DIRECT_REINJECT_ON_MISSING_RECEIVER_062_START */",
    )
    assert "postCommand(cmd)" in route_bridge
    assert 'route: "local_gateway"' in route_bridge
    assert "isDirectInterChatCommand" not in route_bridge
    assert "deliverInterChatDirect" not in route_bridge
    assert "shouldFallbackDirectFailureToGateway" not in route_bridge

    captured = between(
        source,
        'if (message && message.type === "AI_BRIDGE_CAPTURED_ENVELOPE") {',
        'if (message && message.type === "AI_BRIDGE_BRIDGE_COMMAND") {',
    )
    assert 'routeBridgeCommand(validation.envelope, "capturedEnvelope")' in captured
    assert 'if (route === "direct_interchat")' not in captured
    assert "aiBridgeDirectDeliverCapturedEnvelope(validation.envelope)" not in captured

    # Browser execution helpers are intentionally retained for actions claimed by the gateway.
    assert "async function deliverInterChatDirect(cmd)" in source
    assert "async function aiBridgeDirectDeliverCapturedEnvelope(envelope)" in source

    print("SMOKE_EXTENSION_GATEWAY_ONLY_DISPATCH_OK", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

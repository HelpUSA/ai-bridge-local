from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
background = (ROOT / "extension" / "background.js").read_text(encoding="utf-8")

print("SMOKE_GATEWAY_FIRST_ROUTE_GUARDRAILS_START", flush=True)

assert background.count("routeBridgeCommand(") == 3
assert background.count("async function routeBridgeCommand") == 1
assert background.count("await postCommand(cmd)") == 1

route_start = background.index("async function routeBridgeCommand")
route_end = background.index(
    "/* AIBRIDGE_DIRECT_REINJECT_ON_MISSING_RECEIVER_062_START */",
    route_start,
)
route_block = background[route_start:route_end]

assert 'route: "local_gateway"' in route_block
assert "direct: false" in route_block
assert "fallback:" not in route_block
assert "chrome.tabs" not in route_block
assert "injectText(" not in route_block

for forbidden in [
    "mustUseGateway",
    "isDirectInterChatCommand",
    "deliverInterChatDirect",
    "aiBridgeDirectDeliverCapturedEnvelope",
    "aiBridgeDiscoverDirectTargetTab",
    "route_classifier.js",
]:
    assert forbidden not in background, f"forbidden extension route owner: {forbidden}"

print("SMOKE_GATEWAY_FIRST_ROUTE_GUARDRAILS_OK", flush=True)

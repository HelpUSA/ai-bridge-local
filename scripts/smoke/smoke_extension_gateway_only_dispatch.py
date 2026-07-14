from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKGROUND_PATH = ROOT / "extension" / "background.js"
CLASSIFIER_PATH = ROOT / "extension" / "route_classifier.js"

print("SMOKE_EXTENSION_GATEWAY_ONLY_DISPATCH_START", flush=True)

background = BACKGROUND_PATH.read_text(encoding="utf-8")

dead_tokens = [
    "DIRECT_INTERCHAT_ENABLED",
    "DIRECT_INTERCHAT_DISABLED_REASON",
    "DIRECT_INTERCHAT_ALLOW_GATEWAY_FALLBACK",
    "aiBridgeClassifyRouteSafe",
    "isDirectInterChatCommand",
    "mustUseGateway",
    "aiBridgeUrlMatchesDirectTarget",
    "aiBridgeDiscoverDirectTargetTab",
    "deliverInterChatDirect",
    "shouldFallbackDirectFailureToGateway",
    "aiBridgeDirectDeliverCapturedEnvelope",
    "route_classifier.js",
]

for token in dead_tokens:
    assert token not in background, f"legacy direct token remains: {token}"

assert not CLASSIFIER_PATH.exists(), "route_classifier.js must be removed"

route_start = background.index("async function routeBridgeCommand")
route_end = background.index(
    "/* AIBRIDGE_DIRECT_REINJECT_ON_MISSING_RECEIVER_062_START */",
    route_start,
)
route_block = background[route_start:route_end]

assert "await postCommand(cmd)" in route_block
assert 'route: "local_gateway"' in route_block
assert "direct: false" in route_block
assert "pollMessagesSoon" in route_block
assert "injectText(" not in route_block

captured_start = background.index(
    'if (message && message.type === "AI_BRIDGE_CAPTURED_ENVELOPE")'
)
captured_end = background.index(
    'if (message && message.type === "AI_BRIDGE_BRIDGE_COMMAND")',
    captured_start,
)
captured_block = background[captured_start:captured_end]

assert 'routeBridgeCommand(validation.envelope, "capturedEnvelope")' in captured_block
assert "direct_interchat" not in captured_block
assert "injectText(" not in captured_block

command_start = captured_end
command_end = background.index(
    'if (message && message.type === "AI_BRIDGE_REGISTER_CHAT")',
    command_start,
)
command_block = background[command_start:command_end]

assert 'routeBridgeCommand(cmd, "postCommand")' in command_block
assert "direct_interchat" not in command_block
assert "injectText(" not in command_block

assert "async function injectTextOnce" in background
assert "async function injectText" in background
assert "injectText(tabId, action)" in background

print("SMOKE_EXTENSION_GATEWAY_ONLY_DISPATCH_OK", flush=True)

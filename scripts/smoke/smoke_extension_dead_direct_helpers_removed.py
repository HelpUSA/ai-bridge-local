from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
background = (ROOT / "extension" / "background.js").read_text(encoding="utf-8")

print("SMOKE_EXTENSION_DEAD_DIRECT_HELPERS_REMOVED_START", flush=True)

dead_helpers = [
    "boolFlag",
    "shouldForceGateway",
    "isDirectInterChatCommand",
    "mustUseGateway",
    "aiBridgeUrlMatchesDirectTarget",
    "aiBridgeDiscoverDirectTargetTab",
    "deliverInterChatDirect",
    "shouldFallbackDirectFailureToGateway",
    "aiBridgeDirectDeliverCapturedEnvelope",
]

for helper in dead_helpers:
    assert helper not in background, f"dead direct helper remains: {helper}"

required_executor_helpers = [
    "injectTextOnce",
    "injectText",
    "pollMessages",
    "routeBridgeCommand",
]

for helper in required_executor_helpers:
    assert helper in background, f"required executor helper missing: {helper}"

assert not (ROOT / "extension" / "route_classifier.js").exists()

print("SMOKE_EXTENSION_DEAD_DIRECT_HELPERS_REMOVED_OK", flush=True)

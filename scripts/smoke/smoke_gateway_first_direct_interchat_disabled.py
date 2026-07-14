from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
background = (ROOT / "extension" / "background.js").read_text(encoding="utf-8")

print("SMOKE_GATEWAY_FIRST_DIRECT_INTERCHAT_DISABLED_START", flush=True)

for token in [
    "DIRECT_INTERCHAT_ENABLED",
    "DIRECT_INTERCHAT_DISABLED_REASON",
    "DIRECT_INTERCHAT_ALLOW_GATEWAY_FALLBACK",
    "isDirectInterChatCommand",
    "deliverInterChatDirect",
    "aiBridgeDirectDeliverCapturedEnvelope",
    'route: "direct_interchat"',
]:
    assert token not in background, f"direct delivery contract remains: {token}"

assert 'route: "local_gateway"' in background
assert "async function routeBridgeCommand" in background
assert "const gatewayResult = await postCommand(cmd);" in background
assert 'routeBridgeCommand(validation.envelope, "capturedEnvelope")' in background
assert 'routeBridgeCommand(cmd, "postCommand")' in background

print("SMOKE_GATEWAY_FIRST_DIRECT_INTERCHAT_DISABLED_OK", flush=True)

from pathlib import Path

bg = Path("extension/background.js").read_text(encoding="utf-8", errors="replace")

required = [
    "DIRECT_INTERCHAT_ENABLED",
    "DIRECT_INTERCHAT_ALLOW_GATEWAY_FALLBACK = true",
    "function shouldForceGateway",
    "function isDirectInterChatCommand",
    "function mustUseGateway",
    "async function deliverInterChatDirect",
    "async function routeBridgeCommand",
    "routeBridgeCommand(validation.envelope",
    "routeBridgeCommand(cmd, \"postCommand\")",
    "cmd.action === \"run-command\"",
    "cmd.delivery_kind === \"local_capability\"",
    "force_gateway",
    "audit_required",
    "persist_required",
    "require_gateway",
    "target_chat_not_registered",
]

missing = [item for item in required if item not in bg]
if missing:
    raise SystemExit("missing direct interchat router markers: " + ", ".join(missing))

if "postCommand(validation.envelope)" in bg:
    raise SystemExit("captured envelope still posts directly to gateway")
if "postCommand(cmd)\n      .then" in bg:
    raise SystemExit("bridge command still posts directly to gateway")

print("OK smoke_direct_interchat_router")

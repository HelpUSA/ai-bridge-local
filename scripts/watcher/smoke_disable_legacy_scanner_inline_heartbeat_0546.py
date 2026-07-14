from pathlib import Path
import re

cs = Path("extension/content_script.js").read_text(encoding="utf-8", errors="replace")
bg = Path("extension/background.js").read_text(encoding="utf-8", errors="replace")

required = [
    "legacy global body scanner disabled",
    "ChatGPT standalone envelope scanner with visible feedback",
    "installAiBridgeChatGptStandaloneEnvelopeScannerFeedback",
    "AI_BRIDGE_BRIDGE_COMMAND",
    "sendChatHeartbeat unavailable; skipped heartbeat direct_call",
]

missing = [item for item in required if item not in cs]
if missing:
    raise SystemExit("missing 0.5.46 markers: " + ", ".join(missing))

bad = [
    'aiBridgeSafeCallSendChatHeartbeat("direct_call")',
    'aiBridgeSafeCallSendChatHeartbeat("interval")',
    'extract(t).forEach(send);',
    'setInterval(sendChatHeartbeat,',
]

for item in bad:
    if item in cs:
        raise SystemExit("forbidden legacy/unguarded call remains: " + item)

if "routeBridgeCommand" not in bg or "run-command" not in bg or "local_capability" not in bg:
    raise SystemExit("background gateway safety markers missing")

print("OK smoke_disable_legacy_scanner_inline_heartbeat")

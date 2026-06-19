from pathlib import Path
import re

cs = Path("extension/content_script.js").read_text(encoding="utf-8", errors="replace")

required = [
    "function aiBridgeSafeCallSendChatHeartbeat",
    "aiBridgeSafeCallSendChatHeartbeat(\"direct_call\")",
    "aiBridgeSafeCallSendChatHeartbeat(\"interval\")",
    "ChatGPT standalone envelope scanner with visible feedback",
    "installAiBridgeChatGptStandaloneEnvelopeScannerFeedback",
    "AI_BRIDGE_BRIDGE_COMMAND",
]

missing = [item for item in required if item not in cs]
if missing:
    raise SystemExit("missing heartbeat guard markers: " + ", ".join(missing))

bad_direct_calls = re.findall(r"(?<!function\s)\bsendChatHeartbeat\(\);", cs)
if bad_direct_calls:
    raise SystemExit("unguarded sendChatHeartbeat direct call remains")

bad_interval = re.findall(r"setInterval\(\s*sendChatHeartbeat\s*,", cs)
if bad_interval:
    raise SystemExit("unguarded sendChatHeartbeat interval remains")

print("OK smoke_content_script_heartbeat_guard")

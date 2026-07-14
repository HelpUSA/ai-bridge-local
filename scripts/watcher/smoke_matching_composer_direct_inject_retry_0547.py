from pathlib import Path

cs = Path("extension/content_script.js").read_text(encoding="utf-8", errors="replace")
bg = Path("extension/background.js").read_text(encoding="utf-8", errors="replace")

required = [
    "composerAlreadyHasRequestedText",
    "requestedTextBeforeInject",
    "ownedPreflightText = composerAlreadyHasRequestedText",
    "composer_text_matches_requested_text",
    "ChatGPT standalone envelope scanner with visible feedback",
    "legacy global body scanner disabled",
]

missing = [item for item in required if item not in cs]
if missing:
    raise SystemExit("missing 0.5.47 markers: " + ", ".join(missing))

bad = [
    'extract(t).forEach(send);',
    'aiBridgeSafeCallSendChatHeartbeat("direct_call")',
    'setInterval(sendChatHeartbeat,',
]

for item in bad:
    if item in cs:
        raise SystemExit("forbidden old pattern remains: " + item)

if "routeBridgeCommand" not in bg or "run-command" not in bg or "local_capability" not in bg:
    raise SystemExit("background gateway safety markers missing")

print("OK smoke_matching_composer_direct_inject_retry")

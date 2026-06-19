from pathlib import Path

cs = Path("extension/content_script.js").read_text(encoding="utf-8", errors="replace")
bg = Path("extension/background.js").read_text(encoding="utf-8", errors="replace")

marker = "AI Bridge Local: ChatGPT standalone envelope scanner with visible feedback"
if marker not in cs:
    raise SystemExit("missing standalone scanner marker")

standalone = cs.split(marker, 1)[1]

required = [
    "installAiBridgeChatGptStandaloneEnvelopeScannerFeedback",
    "extractEnvelopeBlocks",
    "normalizeCommand",
    "sendCommandToBackground",
    "AI_BRIDGE_BRIDGE_COMMAND",
    "injectVisibleStatus",
    "directOkStatus",
    "errorStatus",
    "bootstrap_existing",
    "ChatGPT standalone envelope scanner with visible feedback installed",
]

missing = [item for item in required if item not in standalone]
if missing:
    raise SystemExit("missing standalone scanner markers: " + ", ".join(missing))

for forbidden in ["typeof extract", "typeof send"]:
    if forbidden in standalone:
        raise SystemExit("standalone scanner still depends on internal " + forbidden)

if "run-command" not in bg or "local_capability" not in bg or "mustUseGateway" not in bg:
    raise SystemExit("background gateway safety markers missing")

print("OK smoke_standalone_scanner_feedback")

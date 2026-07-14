from pathlib import Path

cs = Path("extension/content_script.js").read_text(encoding="utf-8", errors="replace")
bg = Path("extension/background.js").read_text(encoding="utf-8", errors="replace")

marker = "AI Bridge Local: ChatGPT standalone envelope scanner with visible feedback"
if marker not in cs:
    raise SystemExit("standalone marker missing")

standalone = cs.split(marker, 1)[1]

required_global = [
    "legacy global body scanner disabled",
]

required_standalone = [
    "function aiBridgeStandaloneFindPreferredComposer",
    "function aiBridgeStandaloneDescribeComposerElement",
    "function aiBridgeStandaloneUsableComposer",
    "#prompt-textarea.ProseMirror[contenteditable='true']",
    "const aiBridgePreferredComposer = aiBridgeStandaloneFindPreferredComposer();",
    "standalone using preferred ChatGPT composer",
    "injectVisibleStatus",
    "directOkStatus",
    "ChatGPT standalone envelope scanner with visible feedback installed",
]

missing_global = [item for item in required_global if item not in cs]
missing_standalone = [item for item in required_standalone if item not in standalone]
if missing_global or missing_standalone:
    raise SystemExit("missing 0.5.51 markers: " + ", ".join(missing_global + missing_standalone))

for forbidden in [
    "const aiBridgePreferredComposer = aiBridgeFindChatGptPromptTextarea();",
    "aiBridgeDescribeComposerElement(aiBridgePreferredComposer)",
]:
    if forbidden in standalone:
        raise SystemExit("forbidden standalone pattern remains: " + forbidden)

for forbidden in [
    "extract(t).forEach(send);",
    "setInterval(sendChatHeartbeat,",
    'aiBridgeSafeCallSendChatHeartbeat("direct_call")',
]:
    if forbidden in cs:
        raise SystemExit("forbidden old pattern remains: " + forbidden)

if "routeBridgeCommand" not in bg or "run-command" not in bg or "local_capability" not in bg:
    raise SystemExit("background gateway safety markers missing")

print("OK smoke_standalone_visible_status_composer_scope")

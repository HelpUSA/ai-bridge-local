from pathlib import Path

cs = Path("extension/content_script.js").read_text(encoding="utf-8", errors="replace")
bg = Path("extension/background.js").read_text(encoding="utf-8", errors="replace")

required = [
    "function aiBridgeFindChatGptPromptTextarea",
    "function aiBridgeIsUsableComposerCandidate",
    "function aiBridgeDescribeComposerElement",
    "#prompt-textarea.ProseMirror[contenteditable='true']",
    "const aiBridgePreferredComposer = aiBridgeFindChatGptPromptTextarea();",
    "using preferred ChatGPT composer",
    "composer_descriptor: aiBridgeDescribeComposerElement(composer)",
    "ChatGPT standalone envelope scanner with visible feedback",
    "legacy global body scanner disabled",
]

missing = [item for item in required if item not in cs]
if missing:
    raise SystemExit("missing 0.5.49 markers: " + ", ".join(missing))

bad = [
    'extract(t).forEach(send);',
    'setInterval(sendChatHeartbeat,',
    'aiBridgeSafeCallSendChatHeartbeat("direct_call")',
]

for item in bad:
    if item in cs:
        raise SystemExit("forbidden old pattern remains: " + item)

if "mustUseGateway" not in bg or "run-command" not in bg or "local_capability" not in bg:
    raise SystemExit("background gateway safety markers missing")

print("OK smoke_force_chatgpt_prompt_textarea_composer")

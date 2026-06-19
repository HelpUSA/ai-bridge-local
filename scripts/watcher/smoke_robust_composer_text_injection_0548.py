from pathlib import Path

cs = Path("extension/content_script.js").read_text(encoding="utf-8", errors="replace")
bg = Path("extension/background.js").read_text(encoding="utf-8", errors="replace")

required = [
    "function aiBridgeRobustSetText",
    "function aiBridgeDispatchInputEvents",
    "function aiBridgeSetNativeValue",
    "function aiBridgeSetContentEditableByRange",
    "function aiBridgeSetContentEditableByParagraphDom",
    "function aiBridgeSetContentEditableByExecCommand",
    "aiBridgeRobustSetText(composer, text)",
    "aiBridgeRobustSetText(composer, String())",
    "robust_text_injection_enabled",
    "ChatGPT standalone envelope scanner with visible feedback",
    "legacy global body scanner disabled",
]

missing = [item for item in required if item not in cs]
if missing:
    raise SystemExit("missing 0.5.48 markers: " + ", ".join(missing))

bad = [
    "setText(composer, text);",
    "setText(composer, String());",
    'extract(t).forEach(send);',
    'setInterval(sendChatHeartbeat,',
]

for item in bad:
    if item in cs:
        raise SystemExit("forbidden old pattern remains: " + item)

if "mustUseGateway" not in bg or "run-command" not in bg or "local_capability" not in bg:
    raise SystemExit("background gateway safety markers missing")

print("OK smoke_robust_composer_text_injection")

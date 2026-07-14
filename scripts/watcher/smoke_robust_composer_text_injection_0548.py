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

if "routeBridgeCommand" not in bg or "run-command" not in bg or "local_capability" not in bg:
    raise SystemExit("background gateway safety markers missing")

print("OK smoke_robust_composer_text_injection")

# AIBRIDGE_GATEWAY_EXECUTOR_ROBUST_INJECTION_CONTRACT
from pathlib import Path as _AiBridgePath

_ai_bridge_root = _AiBridgePath(__file__).resolve().parents[2]
_ai_bridge_background = (
    _ai_bridge_root / "extension" / "background.js"
).read_text(encoding="utf-8")

_ai_bridge_required_executor_tokens = [
    "async function injectTextOnce",
    "async function injectText",
    "injectText(tabId, action)",
    "aiBridgeLooksLikeMissingReceiverResult",
    "aiBridgeReinjectContentScriptForDirectDelivery",
    'files: ["content_script.js"]',
    "reinjected_content_script",
]

_ai_bridge_missing_executor_tokens = [
    token
    for token in _ai_bridge_required_executor_tokens
    if token not in _ai_bridge_background
]

if _ai_bridge_missing_executor_tokens:
    raise SystemExit(
        "missing gateway executor robust injection markers: "
        + ", ".join(_ai_bridge_missing_executor_tokens)
    )

if ("robust_text_" + "injection_enabled") in _ai_bridge_background:
    raise SystemExit(
        "retired direct-route flag remains in background.js"
    )

print("OK gateway executor robust injection contract")

from pathlib import Path
import re

cs = Path("extension/content_script.js").read_text(encoding="utf-8", errors="replace")
bg = Path("extension/background.js").read_text(encoding="utf-8", errors="replace")

required_content = [
    "var LOCAL_STATUS_PREFIXES = globalThis.__AI_BRIDGE_LOCAL_STATUS_PREFIXES__",
    "globalThis.__AI_BRIDGE_LOCAL_STATUS_PREFIXES__ = LOCAL_STATUS_PREFIXES;",
    "window.__AI_BRIDGE_LOCAL_STATUS_PREFIXES__ = LOCAL_STATUS_PREFIXES;",
    '"[AI_LOCAL_ERRO]"',
    '"[AI_LOCAL_RUN]"',
    '"[AI_LOCAL]"',
    "Gemini envelope observer installed",
    "ChatGPT standalone envelope scanner with visible feedback installed",
    "function aiBridgeStandaloneFindPreferredComposer",
]

missing = [item for item in required_content if item not in cs]
if missing:
    raise SystemExit("missing 0.5.52 content markers: " + ", ".join(missing))

top_prefix = re.search(
    r"^var LOCAL_STATUS_PREFIXES\s*=\s*globalThis\.__AI_BRIDGE_LOCAL_STATUS_PREFIXES__",
    cs,
    re.MULTILINE
)
if not top_prefix:
    raise SystemExit("LOCAL_STATUS_PREFIXES global var not found at top-level")

if "routeBridgeCommand" not in bg or "run-command" not in bg or "local_capability" not in bg:
    raise SystemExit("background gateway safety markers missing")

print("OK smoke_gemini_local_status_prefix_scope")

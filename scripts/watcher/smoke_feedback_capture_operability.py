from pathlib import Path
import json

content = Path("extension/content_script.js").read_text(encoding="utf-8", errors="replace")
background = Path("extension/background.js").read_text(encoding="utf-8", errors="replace")
gateway = Path("gateway_local.py").read_text(encoding="utf-8", errors="replace")
manifest = json.loads(Path("extension/manifest.json").read_text(encoding="utf-8"))
version = Path("VERSION").read_text(encoding="utf-8").strip()

required = {
    "VERSION_FILE_0537": version == "0.5.37",
    "MANIFEST_0537": manifest.get("version") == "0.5.37",
    "CONTENT_0537": "0.5.37" in content,
    "BACKGROUND_0537": "0.5.37" in background,
    "GATEWAY_029": 'VERSION = "0.2.9"' in gateway,
    "ERROR_DEDUPE_TTL": "const ENVELOPE_ERROR_DEDUPE_MS = 30 * 60 * 1000;" in content,
    "ERROR_DEDUPE_TIMES": "const reportedEnvelopeErrorTimes = new Map();" in content,
    "LOCAL_PREFIXES": 'const LOCAL_STATUS_PREFIXES = ["[AI_LOCAL_ERRO]", "[AI_LOCAL_RUN]", "[AI_LOCAL]"];' in content,
    "EXTRACT_SKIPS_LOCAL": "LOCAL_STATUS_PREFIXES.some((prefix) => sourceText.includes(prefix))" in content,
    "GEMINI_SKIPS_LOCAL": "LOCAL_STATUS_PREFIXES.some((prefix) => candidateText.includes(prefix))" in content,
    "GEMINI_CANDIDATES": "const candidateTexts = [];" in content,
    "GEMINI_SMALLEST_FIRST": "candidateTexts.sort((a, b) => a.length - b.length);" in content,
    "SOURCE_FIRST": "const targetCandidates = [info.originalSource, info.currentChatId, info.originalTarget];" in content,
    "BASE64_ADVICE": "payload.command com python -c + base64" in content,
}
missing = [name for name, ok in required.items() if not ok]
if missing:
    raise AssertionError("missing checks: " + ", ".join(missing))
print("SMOKE_FEEDBACK_CAPTURE_OPERABILITY_OK")

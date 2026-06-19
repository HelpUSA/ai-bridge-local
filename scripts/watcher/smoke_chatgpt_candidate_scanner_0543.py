from pathlib import Path

cs = Path("extension/content_script.js").read_text(encoding="utf-8", errors="replace")

required = [
    "ChatGPT candidate envelope periodic scanner",
    "installAiBridgeChatGptCandidateEnvelopeScanner",
    "CANDIDATE_SELECTOR",
    "scanCandidateElements",
    "Candidate scanner extracted",
    "candidateStartsWithLocalStatus",
    "trimmedSourceText.startsWith(prefix)",
]

missing = [item for item in required if item not in cs]
if missing:
    raise SystemExit("missing candidate scanner markers: " + ", ".join(missing))

bad = "LOCAL_STATUS_PREFIXES.some((prefix) => sourceText.includes(prefix))"
if bad in cs:
    raise SystemExit("old global LOCAL_STATUS sourceText guard still present")

print("OK smoke_chatgpt_candidate_scanner")

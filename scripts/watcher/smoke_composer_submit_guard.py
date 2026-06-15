
from pathlib import Path

content = Path("extension/content_script.js").read_text(encoding="utf-8")
background = Path("extension/background.js").read_text(encoding="utf-8")
version = Path("VERSION").read_text(encoding="utf-8").strip()

assert version == "0.5.11", version
assert "0.5.11" in content
assert "0.5.11" in background

required_content = [
    "function isUnsafeSubmitCandidate",
    "function findBlockingModal",
    "function closeBlockingModalIfPresent",
    "share|compartilhar",
    "copy link|copiar link",
    "return -9999",
    ".filter(el => !isUnsafeSubmitCandidate(el))",
    "closeBlockingModalIfPresent();",
]

for marker in required_content:
    assert marker in content, marker

required_background = [
    "let pollInFlight",
    "const perChatInFlight",
    "async function pollOneChat",
    "Promise.allSettled",
]

for marker in required_background:
    assert marker in background, marker

print("OK composer_submit_guard_smoke")

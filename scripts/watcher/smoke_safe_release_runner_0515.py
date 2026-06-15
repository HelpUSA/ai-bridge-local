from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def version_tuple(value):
    return tuple(int(part) for part in value.split("."))

version_bytes = (ROOT / "VERSION").read_bytes()
assert not version_bytes.startswith(b"\xef\xbb\xbf"), version_bytes
VERSION = version_bytes.decode("utf-8").strip()
assert version_tuple(VERSION) >= version_tuple("0.5.15"), VERSION

runner = (ROOT / "scripts" / "release" / "run_safe_release.ps1").read_text(encoding="utf-8-sig")
doc = (ROOT / "docs" / "SAFE_RELEASE_RUNNER_0515.md").read_text(encoding="utf-8-sig")
guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")

required_runner_terms = [
    "Invoke-Native",
    "Assert-NoBomVersion",
    "Invoke-ValidationCommands",
    "git diff --check",
    "git commit -m",
    "git push origin main",
    "AddPaths is empty",
]

for term in required_runner_terms:
    assert term in runner, term

assert "Safe release runner 0.5.15" in doc
assert "sem encerrar o shell" in doc
assert "nao executa entrega inter-chat" in doc
assert "Version alignment 0.5.15" in guide
assert "Safe release runner 0.5.15" in guide
assert "v0.5.15-safe-release-runner" in guide

print("OK safe_release_runner_0515 " + VERSION)
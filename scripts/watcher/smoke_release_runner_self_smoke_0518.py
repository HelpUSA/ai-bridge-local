from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def version_tuple(value):
    return tuple(int(part) for part in value.split("."))

VERSION = (ROOT / "VERSION").read_text(encoding="utf-8-sig").strip()
assert version_tuple(VERSION) >= version_tuple("0.5.18"), VERSION

runner_path = ROOT / "scripts" / "release" / "run_safe_release.ps1"
assert runner_path.exists(), runner_path

runner = runner_path.read_text(encoding="utf-8-sig")
doc = (ROOT / "docs" / "RELEASE_RUNNER_SELF_SMOKE_0518.md").read_text(encoding="utf-8-sig")
guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")

required_terms = [
    "Invoke-Native",
    "Assert-NoBomVersion",
    "Invoke-ValidationCommands",
    "AddPaths is empty",
    "git diff --check",
    "git commit -m",
    "git push origin main",
    "throw",
]

for term in required_terms:
    assert term in runner, term

assert "Release runner self-smoke 0.5.18" in doc
assert "nao executa entrega inter-chat" in doc
assert "Release runner self-smoke 0.5.18" in guide
print("OK release_runner_self_smoke_0518 " + VERSION)
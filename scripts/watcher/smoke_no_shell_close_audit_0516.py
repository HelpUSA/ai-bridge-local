from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]

def version_tuple(value):
    return tuple(int(part) for part in value.split("."))

version_bytes = (ROOT / "VERSION").read_bytes()
assert not version_bytes.startswith(b"\xef\xbb\xbf"), version_bytes
VERSION = version_bytes.decode("utf-8").strip()
assert version_tuple(VERSION) >= version_tuple("0.5.16"), VERSION

manifest = json.loads((ROOT / "extension" / "manifest.json").read_text(encoding="utf-8-sig"))
assert manifest["version"] == VERSION, manifest
assert VERSION in manifest["name"], manifest["name"]

guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")
doc = (ROOT / "docs" / "NO_SHELL_CLOSE_AUDIT_0516.md").read_text(encoding="utf-8-sig")

assert "Version alignment 0.5.16" in guide
assert "No shell close audit 0.5.16" in guide
assert "v0.5.16-no-shell-close-audit" in guide
assert "nao executa entrega inter-chat" in doc

ps1_files = sorted((ROOT / "scripts").rglob("*.ps1"))
assert ps1_files, "no ps1 files found"

for path in ps1_files:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8-sig")
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        assert not re.match(r"(?i)^exit(\s|$)", stripped), (rel, line_number, stripped)

runner = (ROOT / "scripts" / "release" / "run_safe_release.ps1").read_text(encoding="utf-8-sig")
assert "Invoke-Native" in runner
assert "throw" in runner
assert "git diff --check" in runner

print("OK no_shell_close_audit_0516 " + VERSION)
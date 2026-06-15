from pathlib import Path
import ast
import json
import re

ROOT = Path(__file__).resolve().parents[2]

version_bytes = (ROOT / "VERSION").read_bytes()
assert not version_bytes.startswith(b"\xef\xbb\xbf"), version_bytes
VERSION = version_bytes.decode("utf-8").strip()
assert VERSION == "0.5.17", VERSION

manifest = json.loads((ROOT / "extension" / "manifest.json").read_text(encoding="utf-8-sig"))
assert manifest["version"] == VERSION, manifest
assert VERSION in manifest["name"], manifest["name"]

guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")
doc = (ROOT / "docs" / "FORWARD_COMPATIBLE_SMOKE_POLICY_0517.md").read_text(encoding="utf-8-sig")

assert "Version alignment 0.5.17" in guide
assert "Forward-compatible smoke policy 0.5.17" in guide
assert "v0.5.17-forward-compatible-smoke-policy" in guide
assert "nao executa entrega inter-chat" in doc

smoke_files = sorted((ROOT / "scripts" / "watcher").glob("smoke_*_05*.py"))
assert smoke_files, "no micro smoke files found"

locked = []
for path in smoke_files:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue
        comparators = node.comparators
        if len(comparators) != 1:
            continue
        comparator = comparators[0]
        if not isinstance(comparator, ast.Constant) or not isinstance(comparator.value, str):
            continue
        if not re.fullmatch(r"0\.5\.\d+", comparator.value):
            continue
        left_text = ast.get_source_segment(text, node.left) or ""
        if "VERSION" not in left_text:
            continue
        if comparator.value != VERSION:
            locked.append((rel, comparator.value))

assert not locked, locked

print("OK forward_compatible_smoke_policy_0517 0.5.17")
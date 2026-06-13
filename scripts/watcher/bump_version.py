import argparse
import json
import re
from pathlib import Path

ROOT = Path.cwd()
parser = argparse.ArgumentParser()
parser.add_argument("version")
parser.add_argument("--name-prefix", default="AI Bridge Local")
args = parser.parse_args()

version = args.version.strip()
if not re.fullmatch(r"[0-9]+[.][0-9]+[.][0-9]+", version):
    raise SystemExit("version must look like 0.4.40")

manifest_path = ROOT / "extension" / "manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
old_name = manifest.get("name", "")
old_version = manifest.get("version", "")
manifest["version"] = version
manifest["name"] = args.name_prefix + " " + version
manifest_path.write_text(json.dumps(manifest, indent=2) + chr(10), encoding="utf-8")

(ROOT / "VERSION").write_text(version + chr(10), encoding="utf-8")

guide_path = ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md"
text = guide_path.read_text(encoding="utf-8")
heading = "## Version alignment " + version
block = (
    chr(10) + chr(10) + heading + chr(10)
    + "The extension manifest name, extension manifest version, and VERSION file were aligned to "
    + version
    + ". Future releases should use scripts/watcher/bump_version.py and scripts/watcher/smoke_version_alignment.py before tagging."
    + chr(10)
)
if heading not in text:
    text = text.rstrip() + block
guide_path.write_text(text.rstrip() + chr(10), encoding="utf-8")

print("VERSION_BUMP", old_version, "->", version)
print("NAME_BUMP", old_name, "->", manifest["name"])

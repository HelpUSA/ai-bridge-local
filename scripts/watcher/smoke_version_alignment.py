import json
import re
from pathlib import Path

ROOT = Path.cwd()
manifest = json.loads((ROOT / 'extension' / 'manifest.json').read_text(encoding='utf-8-sig'))
version = (ROOT / 'VERSION').read_text(encoding='utf-8-sig').strip().lstrip('ï»¿')
assert re.fullmatch(r'[0-9]+[.][0-9]+[.][0-9]+', version), version
assert manifest.get('version') == version, (manifest.get('version'), version)
name = manifest.get('name', '')
assert version in name, name
guide = (ROOT / 'docs' / 'AI_BRIDGE_LOCAL_GUIDE.md').read_text(encoding='utf-8')
assert version in guide, 'guide missing version'
print('OK version_alignment_smoke', version)

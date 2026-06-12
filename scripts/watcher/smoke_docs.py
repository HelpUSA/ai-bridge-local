from pathlib import Path
ROOT = Path.cwd()
guide = (ROOT / 'docs' / 'AI_BRIDGE_LOCAL_GUIDE.md').read_text(encoding='utf-8')
needles = ['Diagnostics report', 'Safe validation wrapper', 'Command builder smoke', 'Diagnostics filters', 'Diagnostics viewer', 'gateway-brain-supervisor', 'script_text/script_ext', 'Dead letters grouped report']
missing = [n for n in needles if n not in guide]
assert not missing, missing
print('OK docs_smoke')

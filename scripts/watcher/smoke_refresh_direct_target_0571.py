from pathlib import Path
q=chr(34)
bg=Path('extension/background.js').read_text(encoding='utf-8', errors='replace')
cs=Path('extension/content_script.js').read_text(encoding='utf-8', errors='replace')
manifest=Path('extension/manifest.json').read_text(encoding='utf-8', errors='replace')
assert Path('VERSION').read_text(encoding='utf-8').strip()=='0.5.71'
assert 'AI Bridge Local 0.5.71' in manifest
assert 'const VERSION = '+q+'0.5.71'+q+';' in bg
assert 'const VERSION = '+q+'0.5.71'+q+';' in cs
assert 'const CAPTURE_VERSION = '+q+'0.5.71'+q+';' in cs
assert 'const SCANNER_VERSION = '+q+'0.5.71'+q+';' in cs
assert 'const STANDALONE_VERSION = '+q+'0.5.71'+q+';' in cs
assert 'const matches = (tabs || []).filter' in bg
assert 'const activeMatches = matches.filter' in bg
assert 'const match = activeMatches[0] || matches[0];' in bg
assert 'const discoveredTarget = await aiBridgeDiscoverDirectTargetTab' in bg
assert 'else if (!tabId)' in bg
print('OK smoke_refresh_direct_target_0571')

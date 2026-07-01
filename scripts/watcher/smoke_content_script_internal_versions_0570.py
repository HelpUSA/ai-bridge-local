from pathlib import Path
text=Path('extension/content_script.js').read_text(encoding='utf-8', errors='replace')
q=chr(34)
assert 'const VERSION = '+q+'0.5.70'+q+';' in text
assert 'const CAPTURE_VERSION = '+q+'0.5.70'+q+';' in text
assert 'const SCANNER_VERSION = '+q+'0.5.70'+q+';' in text
assert 'const STANDALONE_VERSION = '+q+'0.5.70'+q+';' in text
assert 'const CAPTURE_VERSION = '+q+'0.5.66'+q+';' not in text
assert 'const SCANNER_VERSION = '+q+'0.5.66'+q+';' not in text
assert 'const STANDALONE_VERSION = '+q+'0.5.66'+q+';' not in text
print('OK smoke_content_script_internal_versions_0570')

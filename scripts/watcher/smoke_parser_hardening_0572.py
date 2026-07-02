from pathlib import Path

text = Path("extension/content_script.js").read_text(encoding="utf-8")
assert 'const VERSION = "0.5.75";' in text
assert 'function hasRawLineBreakInLikelyJsonString' in text
assert 'quebra de linha crua dentro de campo JSON' in text
assert 'queued ou sent_direct, sao silenciosos' in text
assert 'replace(/[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f]/g, "")' in text
print("OK smoke_parser_hardening_0572")

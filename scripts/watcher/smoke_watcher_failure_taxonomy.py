from pathlib import Path
doc = Path('docs/WATCHER_FAILURE_TAXONOMY.md').read_text(encoding='utf-8')
report = Path('reports/AI_BRIDGE_LOCAL_WATCHER_FAILURE_TAXONOMY_2026-06-14.md').read_text(encoding='utf-8')
for term in ['envelope_parse_error', 'indentation_loss', 'bom_version_mismatch', 'output_truncated', 'queue_stale_delivering', 'crlf_warning']:
 assert term in doc
assert 'Base64' in doc
assert 'UTF-8 sem BOM' in doc
assert 'audit final read-only' in doc
assert 'taxonomia de falhas' in report
print('OK watcher_failure_taxonomy_smoke')

from pathlib import Path
doc = Path('docs/WATCHER_RECOVERY_RUNBOOK.md').read_text(encoding='utf-8')
report = Path('reports/AI_BRIDGE_LOCAL_WATCHER_RECOVERY_RUNBOOK_2026-06-14.md').read_text(encoding='utf-8')
for term in ['envelope_parse_error', 'indentation_loss', 'bom_version_mismatch', 'output_truncated', 'queue_stale_delivering']:
 assert term in doc
assert 'Base64' in doc
assert 'UTF-8 sem BOM' in doc
assert 'queue_health_audit' in doc
assert 'audit read-only' in report
print('OK watcher_recovery_runbook_smoke')

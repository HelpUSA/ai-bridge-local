from pathlib import Path
q=Path('scripts/watcher/queue_status_report.py')
d=Path('scripts/watcher/dead_letters_cleanup_plan.py')
assert q.exists(), str(q)
assert d.exists(), str(d)
qt=q.read_text(encoding='utf-8')
dt=d.read_text(encoding='utf-8')
assert 'QUEUE_STATUS_REPORT_START' in qt
assert 'DEAD_LETTERS_CLEANUP_PLAN_START' in dt
assert 'dry_run_only' in dt
print('OK queue_reports_cleanup_smoke')

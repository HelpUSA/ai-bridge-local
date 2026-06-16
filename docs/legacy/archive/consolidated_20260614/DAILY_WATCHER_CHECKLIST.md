# Daily Watcher Checklist

1. Run git status -sb and confirm the repo is clean before new work.
2. Run python scripts/watcher/repo_health_report.py.
3. Run python scripts/watcher/cleanup_plan.py --limit 5 in report-only mode.
4. Run python scripts/watcher/backup_queue_db.py before any queue maintenance.
5. Run powershell -NoProfile -ExecutionPolicy Bypass -File scripts/watcher/release_check.ps1 before commit, tag, or handoff.
6. Never clean or edit the queue without a fresh backup and a report-only cleanup plan.
7. After failures, run python scripts/watcher/post_failure_triage.py --limit 5 --prefix ai_bridge_local.

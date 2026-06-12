$ErrorActionPreference='Stop'
$env:PYTHONIOENCODING='utf-8'
Write-Output 'AI_BRIDGE_LOCAL_VALIDATE_ALL_START'
git status -sb
python -m py_compile scripts/watcher/control_center_diagnostics.py
if($LASTEXITCODE -ne 0){throw 'diag_compile_failed'}
python scripts/watcher/control_center_diagnostics.py | Select-Object -First 60
if($LASTEXITCODE -ne 0){throw 'diag_run_failed'}
python scripts/watcher/smoke_command_builder.py
if($LASTEXITCODE -ne 0){throw 'command_builder_smoke_failed'}
python scripts/watcher/smoke_diagnostics_viewer.py
if($LASTEXITCODE -ne 0){throw 'diagnostics_viewer_smoke_failed'}
python scripts/watcher/smoke_docs.py
if($LASTEXITCODE -ne 0){throw 'command_builder_smoke_failed'}
python scripts/watcher/smoke_robustness.py
if($LASTEXITCODE -ne 0){throw 'smoke_failed'}
node --check extension/content_script.js
if($LASTEXITCODE -ne 0){throw 'content_check_failed'}
node --check extension/background.js
if($LASTEXITCODE -ne 0){throw 'background_check_failed'}
python scripts/watcher/health_check.py
if($LASTEXITCODE -ne 0){throw 'health_failed'}
python scripts/watcher/self_heal.py --dry-run
if($LASTEXITCODE -ne 0){throw 'self_heal_failed'}
git diff --check
if($LASTEXITCODE -ne 0){throw 'diff_check_failed'}
Write-Output 'AI_BRIDGE_LOCAL_VALIDATE_ALL_DONE'
python scripts/watcher/smoke_backup_queue_db.py
if($LASTEXITCODE -ne 0){throw 'backup_queue_db_smoke_failed'}
python scripts/watcher/repo_health_report.py
if($LASTEXITCODE -ne 0){throw 'repo_health_report_failed'}
python scripts/watcher/smoke_dead_letters_report.py
if($LASTEXITCODE -ne 0){throw 'dead_letters_report_smoke_failed'}
python scripts/watcher/smoke_cleanup_plan.py
if($LASTEXITCODE -ne 0){throw 'cleanup_plan_smoke_failed'}

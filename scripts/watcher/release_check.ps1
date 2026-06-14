$ErrorActionPreference='Stop'
Write-Output 'AI_BRIDGE_LOCAL_RELEASE_CHECK_START'
git status -sb
python scripts/watcher/repo_health_report.py
if($LASTEXITCODE -ne 0){throw 'repo_health_failed'}
python scripts/watcher/smoke_version_alignment.py
if($LASTEXITCODE -ne 0){throw 'version_alignment_smoke_failed'}
python scripts/watcher/smoke_command_builder.py
if($LASTEXITCODE -ne 0){throw 'command_builder_smoke_failed'}
python scripts/watcher/smoke_command_builder_validate.py
if($LASTEXITCODE -ne 0){throw 'command_builder_validate_smoke_failed'}
python scripts/watcher/smoke_dead_letters_report.py
if($LASTEXITCODE -ne 0){throw 'dead_letters_smoke_failed'}
python scripts/watcher/smoke_cleanup_plan.py
if($LASTEXITCODE -ne 0){throw 'cleanup_plan_smoke_failed'}
python scripts/watcher/smoke_backup_queue_db.py
if($LASTEXITCODE -ne 0){throw 'backup_queue_smoke_failed'}
python scripts/watcher/smoke_docs.py
if($LASTEXITCODE -ne 0){throw 'docs_smoke_failed'}
python scripts/watcher/smoke_examples.py
if($LASTEXITCODE -ne 0){throw 'examples_smoke_failed'}
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/watcher/validate_all.ps1
if($LASTEXITCODE -ne 0){throw 'validate_all_failed'}
git diff --check
if($LASTEXITCODE -ne 0){throw 'diff_check_failed'}
git status -sb
Write-Output 'AI_BRIDGE_LOCAL_RELEASE_CHECK_END'

python scripts/watcher/smoke_command_intake.py
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}

python scripts/watcher/smoke_command_intake_negative.py
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}

python scripts/watcher/smoke_command_builder_output_file.py
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}

python scripts/watcher/smoke_intent_payload.py
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}

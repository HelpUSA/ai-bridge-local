$ErrorActionPreference='Stop'
Write-Output 'AI_BRIDGE_LOCAL_RELEASE_CHECK_START'
git status -sb
python scripts/watcher/repo_health_report.py
if($LASTEXITCODE -ne 0){throw 'repo_health_failed'}
python scripts/watcher/smoke_version_alignment.py
if($LASTEXITCODE -ne 0){throw 'version_alignment_smoke_failed'}
python scripts/watcher/smoke_command_builder.py
if($LASTEXITCODE -ne 0){throw 'command_builder_smoke_failed'}
python scripts/watcher/smoke_send_chat_message.py
if($LASTEXITCODE -ne 0){throw 'send_chat_message_smoke_failed'}
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

python scripts/watcher/smoke_intent_validate_release.py
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
python scripts/watcher/smoke_patch_runner.py
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
python scripts/watcher/smoke_rollback_helper.py
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
python scripts/watcher/smoke_handoff_template.py
if($LASTEXITCODE -ne 0){throw 'smoke_handoff_template_failed'}
python scripts/watcher/smoke_handoff_template.py
if($LASTEXITCODE -ne 0){throw 'smoke_handoff_template_failed'}
python scripts/watcher/smoke_handoff_template.py
if($LASTEXITCODE -ne 0){throw 'smoke_handoff_template_failed'}
python scripts/watcher/smoke_supervision_protocol.py
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
python scripts/watcher/smoke_handoff_template.py
if($LASTEXITCODE -ne 0){throw 'smoke_handoff_template_failed'}
python scripts/watcher/smoke_responsibility_matrix.py
if($LASTEXITCODE -ne 0){throw 'smoke_responsibility_matrix_failed'}
python scripts/watcher/smoke_teach_envelopes.py
if($LASTEXITCODE -ne 0){throw 'smoke_teach_envelopes_failed'}
python scripts/watcher/smoke_teach_envelopes.py
if($LASTEXITCODE -ne 0){throw 'smoke_teach_envelopes_failed'}
python scripts/watcher/smoke_planner_mode.py
if($LASTEXITCODE -ne 0){throw 'smoke_planner_mode_failed'}
python scripts/watcher/smoke_executor_gates.py
if($LASTEXITCODE -ne 0){throw 'smoke_executor_gates_failed'}
python scripts/watcher/smoke_auditor_mode.py
if($LASTEXITCODE -ne 0){throw 'smoke_auditor_mode_failed'}
python scripts/watcher/smoke_release_manager_mode.py
if($LASTEXITCODE -ne 0){throw 'smoke_release_manager_mode_failed'}
python scripts/watcher/smoke_hardening_tools.py
if($LASTEXITCODE -ne 0){throw 'smoke_hardening_tools_failed'}
python scripts/watcher/smoke_local_api_foundations.py
if($LASTEXITCODE -ne 0){throw 'smoke_local_api_foundations_failed'}
python scripts/watcher/smoke_local_bridge_store.py
if($LASTEXITCODE -ne 0){throw 'smoke_local_bridge_store_failed'}
python scripts/watcher/smoke_local_bridge_envelope.py
if($LASTEXITCODE -ne 0){throw 'smoke_local_bridge_envelope_failed'}
python scripts/watcher/smoke_local_bridge_writer_ack.py
if($LASTEXITCODE -ne 0){throw 'smoke_local_bridge_writer_ack_failed'}
python scripts/watcher/smoke_local_bridge_dashboard.py
if($LASTEXITCODE -ne 0){throw 'smoke_local_bridge_dashboard_failed'}
python scripts/watcher/smoke_local_bridge_replay_apply.py
if($LASTEXITCODE -ne 0){throw 'smoke_local_bridge_replay_apply_failed'}
python scripts/watcher/smoke_local_bridge_worker_dry_run.py
if($LASTEXITCODE -ne 0){throw 'smoke_local_bridge_worker_dry_run_failed'}
python scripts/watcher/smoke_governance_risk_classifier.py
if($LASTEXITCODE -ne 0){throw 'smoke_governance_risk_classifier_failed'}
python scripts/watcher/smoke_governance_preflight.py
if($LASTEXITCODE -ne 0){throw 'smoke_governance_preflight_failed'}

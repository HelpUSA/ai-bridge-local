$ErrorActionPreference='Stop'
$env:PYTHONIOENCODING='utf-8'
Write-Output 'AI_BRIDGE_LOCAL_VALIDATE_ALL_START'
git status -sb
python -m py_compile scripts/watcher/control_center_diagnostics.py
if($LASTEXITCODE -ne 0){throw 'diag_compile_failed'}
python scripts/watcher/control_center_diagnostics.py | Select-Object -First 60
if($LASTEXITCODE -ne 0){throw 'diag_run_failed'}
python scripts/watcher/smoke_version_alignment.py
if($LASTEXITCODE -ne 0){throw 'version_alignment_smoke_failed'}
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
python scripts/watcher/smoke_command_builder_governance.py
if($LASTEXITCODE -ne 0){throw 'smoke_command_builder_governance_failed'}
python scripts/watcher/smoke_command_builder_advisory.py
if($LASTEXITCODE -ne 0){throw 'smoke_command_builder_advisory_failed'}
python scripts/watcher/smoke_command_builder_advisory_gate.py
if($LASTEXITCODE -ne 0){throw 'smoke_command_builder_advisory_gate_failed'}
python scripts/watcher/smoke_governance_decision_log.py
if($LASTEXITCODE -ne 0){throw 'smoke_governance_decision_log_failed'}
python scripts/watcher/smoke_governance_risk_report.py
if($LASTEXITCODE -ne 0){throw 'smoke_governance_risk_report_failed'}
python scripts/watcher/smoke_command_builder_preferred.py
if($LASTEXITCODE -ne 0){throw 'smoke_command_builder_preferred_failed'}
python scripts/watcher/smoke_command_builder_destructive_optin_gate.py
if($LASTEXITCODE -ne 0){throw 'smoke_command_builder_destructive_optin_gate_failed'}
python scripts/watcher/smoke_queue_health_audit.py
if($LASTEXITCODE -ne 0){throw 'smoke_queue_health_audit_failed'}
python scripts/watcher/smoke_safe_envelope_templates.py
if($LASTEXITCODE -ne 0){throw 'smoke_safe_envelope_templates_failed'}
python scripts/watcher/smoke_governance_enforcement_dry_run.py
if($LASTEXITCODE -ne 0){throw 'smoke_governance_enforcement_dry_run_failed'}
python scripts/watcher/smoke_release_safety_checklist.py
if($LASTEXITCODE -ne 0){throw 'smoke_release_safety_checklist_failed'}
python scripts/watcher/smoke_queue_triage_playbook.py
if($LASTEXITCODE -ne 0){throw 'smoke_queue_triage_playbook_failed'}
python scripts/watcher/smoke_watcher_failure_taxonomy.py
if($LASTEXITCODE -ne 0){throw 'smoke_watcher_failure_taxonomy_failed'}
python scripts/watcher/smoke_self_evolution_guardrails.py
if($LASTEXITCODE -ne 0){throw 'smoke_self_evolution_guardrails_failed'}
python scripts/watcher/smoke_watcher_recovery_runbook.py
if($LASTEXITCODE -ne 0){throw 'smoke_watcher_recovery_runbook_failed'}
python scripts/watcher/smoke_autonomous_evolution_protocol.py
if($LASTEXITCODE -ne 0){throw 'smoke_autonomous_evolution_protocol_failed'}
python scripts/watcher/smoke_autonomous_evolution_approval_matrix.py
if($LASTEXITCODE -ne 0){throw 'smoke_autonomous_evolution_approval_matrix_failed'}
python scripts/watcher/smoke_autonomous_change_proposal_template.py
if($LASTEXITCODE -ne 0){throw 'smoke_autonomous_change_proposal_template_failed'}
python scripts/watcher/smoke_autonomous_evolution_task_queue.py
if($LASTEXITCODE -ne 0){throw 'smoke_autonomous_evolution_task_queue_failed'}
python scripts/watcher/smoke_autonomous_evolution_audit_ledger.py
if($LASTEXITCODE -ne 0){throw 'smoke_autonomous_evolution_audit_ledger_failed'}
python scripts/watcher/smoke_latency_parallel_polling.py
if($LASTEXITCODE -ne 0){throw 'smoke_latency_parallel_polling_failed'}
python scripts/watcher/smoke_latency_parallel_polling_docs.py
if($LASTEXITCODE -ne 0){throw 'smoke_latency_parallel_polling_docs_failed'}

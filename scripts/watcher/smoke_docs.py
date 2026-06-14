from pathlib import Path
ROOT = Path.cwd()
guide_path = ROOT / 'docs' / 'AI_BRIDGE_LOCAL_GUIDE.md'
version_path = ROOT / 'VERSION'
guide = guide_path.read_text(encoding='utf-8')
version = version_path.read_text(encoding='utf-8').strip()
required_text = ['# AI Bridge Local - Guia Unificado Operacional e Roadmap', 'Marco publicado mais recente:', 'Commit de referencia:', 'Diagnostics report', 'Safe validation wrapper', 'Command builder smoke', 'Diagnostics filters', 'Diagnostics viewer', 'gateway-brain-supervisor', 'script_text/script_ext', 'Dead letters grouped report', 'rollback_helper.py', 'patch_runner.py', 'supervision_protocol.py', 'handoff_template.py', 'responsibility_matrix.py', 'teach_envelopes.py', 'planner_mode.py', 'executor_gates.py', 'auditor_mode.py', 'release_manager_mode.py', 'post_release_audit.py', 'tag_divergence_report.py', 'dead_letters_review.py', 'local_api_readonly.py', 'local_api_dry_run.py', 'chat_bridge_plan.py', 'local_bridge_store.py', 'local_bridge_reconcile.py', 'local_bridge_envelope.py', 'local_bridge_replay_dry_run.py', 'local_bridge_writer.py', 'local_bridge_ack_writer.py', 'local_bridge_dashboard.py', 'local_bridge_dashboard_summary.py', 'local_bridge_replay_apply.py', 'local_bridge_worker_dry_run.py', 'governance_risk_classifier.py', 'governance_preflight.py', 'smoke_command_builder_governance.py', 'teach_envelopes.py', 'planner_mode.py', 'executor_gates.py', 'auditor_mode.py', 'release_manager_mode.py', 'post_release_audit.py', 'tag_divergence_report.py', 'dead_letters_review.py', 'local_api_readonly.py', 'local_api_dry_run.py', 'chat_bridge_plan.py', 'local_bridge_store.py', 'local_bridge_reconcile.py', 'local_bridge_envelope.py', 'local_bridge_replay_dry_run.py', 'local_bridge_writer.py', 'local_bridge_ack_writer.py', 'local_bridge_dashboard.py', 'local_bridge_dashboard_summary.py', 'local_bridge_replay_apply.py', 'local_bridge_worker_dry_run.py', 'governance_risk_classifier.py', 'governance_preflight.py', 'smoke_command_builder_governance.py', '## 14. Proximas atividades recomendadas em ordem', '## Version alignment ' + version]
missing = [needle for needle in required_text if needle not in guide]
assert not missing, 'missing required guide text: ' + repr(missing)
required_headings = ['## 1. Objetivo do projeto', '## 2. Estado atual validado', '## 4. Protocolo de envelopes', '## 9. Roadmap detalhado de atividades pendentes', '### 9.7 Longo prazo - orquestracao entre chats', '## 14. Proximas atividades recomendadas em ordem']
missing_headings = [heading for heading in required_headings if heading not in guide]
assert not missing_headings, 'missing required headings: ' + repr(missing_headings)
guide_lines = guide.splitlines()
latest_lines = [line for line in guide_lines if line.startswith('Marco publicado mais recente:')]
assert latest_lines, 'missing latest release marker'
latest_marker = latest_lines[0].split(':', 1)[1].strip().split()[0]
assert latest_marker.startswith('v' + version + '-'), (version, latest_marker)
commit_lines = [line for line in guide_lines if line.startswith('Commit de referencia:')]
assert commit_lines, 'missing reference commit line'
commit_ref = commit_lines[0].split(':', 1)[1].strip()
assert not commit_ref.lower().startswith('pendente'), commit_ref
first_token = commit_ref.split()[0] if commit_ref.split() else ''
assert len(first_token) >= 7, commit_ref
versions = ['0.4.45', '0.4.46', '0.4.47', '0.4.48', '0.4.49', '0.4.50', '0.4.51', '0.4.52', '0.4.53', '0.4.54', '0.4.55', '0.4.56', '0.4.57', '0.4.58', '0.4.59', '0.4.60', '0.4.61', '0.4.62', '0.4.63', '0.4.64', '0.4.65', '0.4.66', '0.4.67', '0.4.68', '0.4.69', '0.4.70', '0.4.72', '0.4.73', '0.4.74', '0.4.75', '0.4.76', '0.4.77', '0.4.78', '0.4.79', '0.4.80', version]
dupes = [v for v in versions if ('[DONE ' + v + '] [DONE ' + v + ']') in guide]
assert not dupes, 'duplicate DONE markers found: ' + repr(dupes)
items = ['1. Criar smoke para send-chat-message. [DONE 0.4.45]', '2. Criar intent inspect_delivery_failure. [DONE 0.4.46]', '3. Melhorar diagnostico de submit_button_not_found_or_disabled. [DONE 0.4.47]', '4. Criar intent validate_release. [DONE 0.4.48]', '5. Criar patch runner com dry-run. [DONE 0.4.49]', '6. Criar rollback helper. [DONE 0.4.50]', '7. Consolidar relatorio de dead letters por tipo. [DONE 0.4.51]', '8. Criar protocolo formal de fiscalizacao entre chats. [DONE 0.4.52]', '9. Melhorar docs smoke para garantir que este guia continue completo. [DONE 0.4.53]', '10. Remover referencias obsoletas de release antiga e compatibilidade do docs smoke. [DONE 0.4.54]', '11. Criar padrao de handoff entre chats. [DONE 0.4.56]', '12. Criar matriz de responsabilidade entre chats. [DONE 0.4.57]', '13. Criar envelopes de ensino. [DONE 0.4.58]', '14. Criar modo planejador. [DONE 0.4.59]', '15. Criar modo executor com gates. [DONE 0.4.60]', '16. Criar modo auditor. [DONE 0.4.61]', '17. Criar modo release manager. [DONE 0.4.62]']
missing_items = [item for item in items if item not in guide]
assert not missing_items, 'missing roadmap done markers: ' + repr(missing_items)
stale_text = ['Criar release 0.4.45 somente depois de smokes e release_check OK.', 'compatibilidade com smoke_docs.py ate que']
stale_found = [stale for stale in stale_text if stale in guide]
assert not stale_found, 'stale guide text found: ' + repr(stale_found)

assert guide.count('2. Criar padrao de handoff. [DONE 0.4.56 - template cli json markdown]') == 1, 'duplicate handoff 9.7 marker'
assert guide.count('11. Criar padrao de handoff entre chats. [DONE 0.4.56]') == 1, 'duplicate handoff section 14 marker'
print('OK docs_smoke', version, latest_marker)

version_alignment_heading_count = guide.count('## Version alignment ' + version)
assert version_alignment_heading_count == 1, 'version alignment heading count: ' + str(version_alignment_heading_count)
responsibility_item_9_7 = '3. Criar matriz de responsabilidade. [DONE 0.4.57 - supervisor executor fiscal documentador]'
responsibility_item_14 = '12. Criar matriz de responsabilidade entre chats. [DONE 0.4.57]'
responsibility_item_9_7_count = guide.count(responsibility_item_9_7)
responsibility_item_14_count = guide.count(responsibility_item_14)
assert responsibility_item_9_7_count == 1, 'responsibility 9.7 marker count: ' + str(responsibility_item_9_7_count)
assert responsibility_item_14_count == 1, 'responsibility section 14 marker count: ' + str(responsibility_item_14_count)
teach_item_9_7 = '4. Criar envelopes de ensino. [DONE 0.4.58 - watcher safety release recovery lessons]'
teach_item_14 = '13. Criar envelopes de ensino. [DONE 0.4.58]'
teach_item_9_7_count = guide.count(teach_item_9_7)
teach_item_14_count = guide.count(teach_item_14)
assert teach_item_9_7_count == 1, 'teach 9.7 marker count: ' + str(teach_item_9_7_count)
assert teach_item_14_count == 1, 'teach section 14 marker count: ' + str(teach_item_14_count)
teach_item_9_7 = '4. Criar envelopes de ensino. [DONE 0.4.58 - watcher safety release recovery lessons]'
teach_item_14 = '13. Criar envelopes de ensino. [DONE 0.4.58]'
teach_item_9_7_count = guide.count(teach_item_9_7)
teach_item_14_count = guide.count(teach_item_14)
assert teach_item_9_7_count == 1, 'teach 9.7 marker count: ' + str(teach_item_9_7_count)
assert teach_item_14_count == 1, 'teach section 14 marker count: ' + str(teach_item_14_count)
teach_alignment_count = guide.count('## Version alignment 0.4.58')
assert teach_alignment_count == 1, 'teach version alignment count: ' + str(teach_alignment_count)
teach_file_line_count = guide.count('- scripts/watcher/teach_envelopes.py.')
assert teach_file_line_count == 1, 'teach file line count: ' + str(teach_file_line_count)
planner_item_9_8 = '1. Criar modo planejador. [DONE 0.4.59 - read-only objective plan gates]'
planner_item_14 = '14. Criar modo planejador. [DONE 0.4.59]'
planner_item_9_8_count = guide.count(planner_item_9_8)
planner_item_14_count = guide.count(planner_item_14)
planner_alignment_count = guide.count('## Version alignment 0.4.59')
planner_file_line_count = guide.count('- scripts/watcher/planner_mode.py.')
assert planner_item_9_8_count == 1, 'planner 9.8 marker count: ' + str(planner_item_9_8_count)
assert planner_item_14_count == 1, 'planner section 14 marker count: ' + str(planner_item_14_count)
assert planner_alignment_count == 1, 'planner alignment count: ' + str(planner_alignment_count)
assert planner_file_line_count == 1, 'planner file line count: ' + str(planner_file_line_count)
executor_item_9_8 = '2. Criar modo executor com gates. [DONE 0.4.60 - approval validation stop-on-failure gates]'
executor_item_14 = '15. Criar modo executor com gates. [DONE 0.4.60]'
executor_item_9_8_count = guide.count(executor_item_9_8)
executor_item_14_count = guide.count(executor_item_14)
executor_alignment_count = guide.count('## Version alignment 0.4.60')
executor_file_line_count = guide.count('- scripts/watcher/executor_gates.py.')
assert executor_item_9_8_count == 1, 'executor 9.8 marker count: ' + str(executor_item_9_8_count)
assert executor_item_14_count == 1, 'executor section 14 marker count: ' + str(executor_item_14_count)
assert executor_alignment_count == 1, 'executor alignment count: ' + str(executor_alignment_count)
assert executor_file_line_count == 1, 'executor file line count: ' + str(executor_file_line_count)
auditor_item_9_8 = '3. Criar modo auditor. [DONE 0.4.61 - git tags docs divergence audit]'
auditor_item_14 = '16. Criar modo auditor. [DONE 0.4.61]'
auditor_item_9_8_count = guide.count(auditor_item_9_8)
auditor_item_14_count = guide.count(auditor_item_14)
auditor_alignment_count = guide.count('## Version alignment 0.4.61')
auditor_file_line_count = guide.count('- scripts/watcher/auditor_mode.py.')
assert auditor_item_9_8_count == 1, 'auditor 9.8 marker count: ' + str(auditor_item_9_8_count)
assert auditor_item_14_count == 1, 'auditor section 14 marker count: ' + str(auditor_item_14_count)
assert auditor_alignment_count == 1, 'auditor alignment count: ' + str(auditor_alignment_count)
assert auditor_file_line_count == 1, 'auditor file line count: ' + str(auditor_file_line_count)
release_manager_item_9_8 = '4. Criar modo release manager. [DONE 0.4.62 - safe single-commit release plan]'
release_manager_item_14 = '17. Criar modo release manager. [DONE 0.4.62]'
release_manager_item_9_8_count = guide.count(release_manager_item_9_8)
release_manager_item_14_count = guide.count(release_manager_item_14)
release_manager_alignment_count = guide.count('## Version alignment 0.4.62')
release_manager_file_line_count = guide.count('- scripts/watcher/release_manager_mode.py.')
assert release_manager_item_9_8_count == 1, 'release manager 9.8 marker count: ' + str(release_manager_item_9_8_count)
assert release_manager_item_14_count == 1, 'release manager section 14 marker count: ' + str(release_manager_item_14_count)
assert release_manager_alignment_count == 1, 'release manager alignment count: ' + str(release_manager_alignment_count)
assert release_manager_file_line_count == 1, 'release manager file line count: ' + str(release_manager_file_line_count)
hardening_alignment_count = guide.count('## Version alignment 0.4.63')
hardening_section_count = guide.count('## 16. Hardening pos fase 9.8')
hardening_report_count = guide.count('reports/AI_BRIDGE_LOCAL_PHASE_9_8_FINAL_2026-06-14.md')
assert hardening_alignment_count == 1, 'hardening alignment count: ' + str(hardening_alignment_count)
assert hardening_section_count == 1, 'hardening section count: ' + str(hardening_section_count)
assert hardening_report_count >= 1, 'hardening report reference missing'
local_api_alignment_count = guide.count('## Version alignment 0.4.64')
local_api_section_count = guide.count('## 17. Proxima fase - fundamentos API local')
local_api_report_count = guide.count('reports/AI_BRIDGE_LOCAL_NEXT_PHASE_BLOCKS_2026-06-14.md')
assert local_api_alignment_count == 1, 'local api alignment count: ' + str(local_api_alignment_count)
assert local_api_section_count == 1, 'local api section count: ' + str(local_api_section_count)
assert local_api_report_count >= 1, 'local api report reference missing'
local_bridge_alignment_count = guide.count('## Version alignment 0.4.65')
local_bridge_section_count = guide.count('## 18. Local bridge store')
local_bridge_report_count = guide.count('reports/AI_BRIDGE_LOCAL_LOCAL_BRIDGE_STORE_2026-06-14.md')
assert local_bridge_alignment_count == 1, 'local bridge alignment count: ' + str(local_bridge_alignment_count)
assert local_bridge_section_count == 1, 'local bridge section count: ' + str(local_bridge_section_count)
assert local_bridge_report_count >= 1, 'local bridge report reference missing'
local_bridge_envelope_alignment_count = guide.count('## Version alignment 0.4.66')
local_bridge_envelope_section_count = guide.count('## 19. Local bridge envelope')
local_bridge_envelope_report_count = guide.count('reports/AI_BRIDGE_LOCAL_LOCAL_BRIDGE_ENVELOPE_2026-06-14.md')
assert local_bridge_envelope_alignment_count == 1, 'local bridge envelope alignment count: ' + str(local_bridge_envelope_alignment_count)
assert local_bridge_envelope_section_count == 1, 'local bridge envelope section count: ' + str(local_bridge_envelope_section_count)
assert local_bridge_envelope_report_count >= 1, 'local bridge envelope report reference missing'
local_bridge_writer_ack_alignment_count = guide.count('## Version alignment 0.4.67')
local_bridge_writer_ack_section_count = guide.count('## 20. Local bridge writer e ack')
local_bridge_writer_ack_report_count = guide.count('reports/AI_BRIDGE_LOCAL_LOCAL_BRIDGE_WRITER_ACK_2026-06-14.md')
assert local_bridge_writer_ack_alignment_count == 1, 'local bridge writer ack alignment count: ' + str(local_bridge_writer_ack_alignment_count)
assert local_bridge_writer_ack_section_count == 1, 'local bridge writer ack section count: ' + str(local_bridge_writer_ack_section_count)
assert local_bridge_writer_ack_report_count >= 1, 'local bridge writer ack report reference missing'
local_bridge_dashboard_alignment_count = guide.count('## Version alignment 0.4.68')
local_bridge_dashboard_section_count = guide.count('## 21. Local bridge dashboard')
local_bridge_dashboard_report_count = guide.count('reports/AI_BRIDGE_LOCAL_LOCAL_BRIDGE_DASHBOARD_2026-06-14.md')
assert local_bridge_dashboard_alignment_count == 1, 'local bridge dashboard alignment count: ' + str(local_bridge_dashboard_alignment_count)
assert local_bridge_dashboard_section_count == 1, 'local bridge dashboard section count: ' + str(local_bridge_dashboard_section_count)
assert local_bridge_dashboard_report_count >= 1, 'local bridge dashboard report reference missing'
local_bridge_replay_apply_alignment_count = guide.count('## Version alignment 0.4.69')
local_bridge_replay_apply_section_count = guide.count('## 22. Local bridge replay apply')
local_bridge_replay_apply_report_count = guide.count('reports/AI_BRIDGE_LOCAL_LOCAL_BRIDGE_REPLAY_APPLY_2026-06-14.md')
assert local_bridge_replay_apply_alignment_count == 1, 'local bridge replay apply alignment count: ' + str(local_bridge_replay_apply_alignment_count)
assert local_bridge_replay_apply_section_count == 1, 'local bridge replay apply section count: ' + str(local_bridge_replay_apply_section_count)
assert local_bridge_replay_apply_report_count >= 1, 'local bridge replay apply report reference missing'
local_bridge_worker_dry_run_alignment_count = guide.count('## Version alignment 0.4.70')
local_bridge_worker_dry_run_section_count = guide.count('## 23. Local bridge worker dry-run')
local_bridge_worker_dry_run_report_count = guide.count('reports/AI_BRIDGE_LOCAL_LOCAL_BRIDGE_WORKER_DRY_RUN_2026-06-14.md')
assert local_bridge_worker_dry_run_alignment_count == 1, 'local bridge worker dry run alignment count: ' + str(local_bridge_worker_dry_run_alignment_count)
assert local_bridge_worker_dry_run_section_count == 1, 'local bridge worker dry run section count: ' + str(local_bridge_worker_dry_run_section_count)
assert local_bridge_worker_dry_run_report_count >= 1, 'local bridge worker dry run report reference missing'
local_bridge_consolidation_section_count = guide.count('## 24. Consolidacao local bridge 0.4.65 a 0.4.70')
local_bridge_consolidation_alignment_count = guide.count('## Version alignment 0.4.71')
local_bridge_consolidation_report_count = guide.count('reports/AI_BRIDGE_LOCAL_LOCAL_BRIDGE_CONSOLIDATION_2026-06-14.md')
assert local_bridge_consolidation_section_count == 1, 'local bridge consolidation section count: ' + str(local_bridge_consolidation_section_count)
assert local_bridge_consolidation_alignment_count == 1, 'local bridge consolidation alignment count: ' + str(local_bridge_consolidation_alignment_count)
assert local_bridge_consolidation_report_count >= 1, 'local bridge consolidation report reference missing'
governance_risk_classifier_alignment_count = guide.count('## Version alignment 0.4.72')
governance_risk_classifier_section_count = guide.count('## 25. Governance risk classifier')
governance_risk_classifier_report_count = guide.count('reports/AI_BRIDGE_LOCAL_GOVERNANCE_RISK_CLASSIFIER_2026-06-14.md')
assert governance_risk_classifier_alignment_count == 1, 'governance risk classifier alignment count: ' + str(governance_risk_classifier_alignment_count)
assert governance_risk_classifier_section_count == 1, 'governance risk classifier section count: ' + str(governance_risk_classifier_section_count)
assert governance_risk_classifier_report_count >= 1, 'governance risk classifier report reference missing'
governance_preflight_alignment_count = guide.count('## Version alignment 0.4.73')
governance_preflight_section_count = guide.count('## 26. Governance preflight')
governance_preflight_report_count = guide.count('reports/AI_BRIDGE_LOCAL_GOVERNANCE_PREFLIGHT_2026-06-14.md')
assert governance_preflight_alignment_count == 1, 'governance preflight alignment count: ' + str(governance_preflight_alignment_count)
assert governance_preflight_section_count == 1, 'governance preflight section count: ' + str(governance_preflight_section_count)
assert governance_preflight_report_count >= 1, 'governance preflight report reference missing'
command_builder_governance_alignment_count = guide.count('## Version alignment 0.4.74')
command_builder_governance_section_count = guide.count('## 27. Command builder governance')
command_builder_governance_report_count = guide.count('reports/AI_BRIDGE_LOCAL_COMMAND_BUILDER_GOVERNANCE_2026-06-14.md')
assert command_builder_governance_alignment_count == 1, 'command builder governance alignment count: ' + str(command_builder_governance_alignment_count)
assert command_builder_governance_section_count == 1, 'command builder governance section count: ' + str(command_builder_governance_section_count)
assert command_builder_governance_report_count >= 1, 'command builder governance report reference missing'
command_builder_governance_finalize_alignment_count = guide.count('## Version alignment 0.4.75')
command_builder_governance_finalize_section_count = guide.count('## 28. Command builder governance finalize')
command_builder_governance_finalize_report_count = guide.count('reports/AI_BRIDGE_LOCAL_COMMAND_BUILDER_GOVERNANCE_FINALIZE_2026-06-14.md')
assert command_builder_governance_finalize_alignment_count == 1, 'command builder governance finalize alignment count: ' + str(command_builder_governance_finalize_alignment_count)
assert command_builder_governance_finalize_section_count == 1, 'command builder governance finalize section count: ' + str(command_builder_governance_finalize_section_count)
assert command_builder_governance_finalize_report_count >= 1, 'command builder governance finalize report reference missing'
governance_roadmap_alignment_count = guide.count('## Version alignment 0.4.76')
governance_roadmap_section_count = guide.count('## 29. Governance roadmap')
governance_roadmap_report_count = guide.count('reports/AI_BRIDGE_LOCAL_GOVERNANCE_ROADMAP_2026-06-14.md')
assert governance_roadmap_alignment_count == 1, 'governance roadmap alignment count: ' + str(governance_roadmap_alignment_count)
assert governance_roadmap_section_count == 1, 'governance roadmap section count: ' + str(governance_roadmap_section_count)
assert governance_roadmap_report_count >= 1, 'governance roadmap report reference missing'
command_builder_advisory_alignment_count = guide.count('## Version alignment 0.4.77')
command_builder_advisory_section_count = guide.count('## 30. Command builder advisory metadata')
command_builder_advisory_report_count = guide.count('reports/AI_BRIDGE_LOCAL_COMMAND_BUILDER_ADVISORY_2026-06-14.md')
assert command_builder_advisory_alignment_count == 1, 'command builder advisory alignment count: ' + str(command_builder_advisory_alignment_count)
assert command_builder_advisory_section_count == 1, 'command builder advisory section count: ' + str(command_builder_advisory_section_count)
assert command_builder_advisory_report_count >= 1, 'command builder advisory report reference missing'
command_builder_advisory_gate_alignment_count = guide.count('## Version alignment 0.4.78')
command_builder_advisory_gate_section_count = guide.count('## 31. Command builder advisory gate')
command_builder_advisory_gate_report_count = guide.count('reports/AI_BRIDGE_LOCAL_COMMAND_BUILDER_ADVISORY_GATE_2026-06-14.md')
assert command_builder_advisory_gate_alignment_count == 1, 'command_builder_advisory_gate alignment count: ' + str(command_builder_advisory_gate_alignment_count)
assert command_builder_advisory_gate_section_count == 1, 'command_builder_advisory_gate section count: ' + str(command_builder_advisory_gate_section_count)
assert command_builder_advisory_gate_report_count >= 1, 'command_builder_advisory_gate report reference missing'
governance_decision_log_alignment_count = guide.count('## Version alignment 0.4.79')
governance_decision_log_section_count = guide.count('## 32. Governance decision log')
governance_decision_log_report_count = guide.count('reports/AI_BRIDGE_LOCAL_GOVERNANCE_DECISION_LOG_2026-06-14.md')
assert governance_decision_log_alignment_count == 1, 'governance_decision_log alignment count: ' + str(governance_decision_log_alignment_count)
assert governance_decision_log_section_count == 1, 'governance_decision_log section count: ' + str(governance_decision_log_section_count)
assert governance_decision_log_report_count >= 1, 'governance_decision_log report reference missing'
governance_risk_report_alignment_count = guide.count('## Version alignment 0.4.80')
governance_risk_report_section_count = guide.count('## 33. Governance risk report')
governance_risk_report_report_count = guide.count('reports/AI_BRIDGE_LOCAL_GOVERNANCE_RISK_REPORT_2026-06-14.md')
assert governance_risk_report_alignment_count == 1, 'governance_risk_report alignment count: ' + str(governance_risk_report_alignment_count)
assert governance_risk_report_section_count == 1, 'governance_risk_report section count: ' + str(governance_risk_report_section_count)
assert governance_risk_report_report_count >= 1, 'governance_risk_report report reference missing'

from pathlib import Path
ROOT = Path.cwd()
guide_path = ROOT / 'docs' / 'AI_BRIDGE_LOCAL_GUIDE.md'
version_path = ROOT / 'VERSION'
guide = guide_path.read_text(encoding='utf-8')
version = version_path.read_text(encoding='utf-8').strip()
required_text = ['# AI Bridge Local - Guia Unificado Operacional e Roadmap', 'Marco publicado mais recente:', 'Commit de referencia:', 'Diagnostics report', 'Safe validation wrapper', 'Command builder smoke', 'Diagnostics filters', 'Diagnostics viewer', 'gateway-brain-supervisor', 'script_text/script_ext', 'Dead letters grouped report', 'rollback_helper.py', 'patch_runner.py', 'supervision_protocol.py', 'handoff_template.py', 'responsibility_matrix.py', 'teach_envelopes.py', 'planner_mode.py', 'executor_gates.py', 'auditor_mode.py', 'release_manager_mode.py', 'teach_envelopes.py', 'planner_mode.py', 'executor_gates.py', 'auditor_mode.py', 'release_manager_mode.py', '## 14. Proximas atividades recomendadas em ordem', '## Version alignment ' + version]
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
versions = ['0.4.45', '0.4.46', '0.4.47', '0.4.48', '0.4.49', '0.4.50', '0.4.51', '0.4.52', '0.4.53', '0.4.54', '0.4.55', '0.4.56', '0.4.57', '0.4.58', '0.4.59', '0.4.60', '0.4.61', '0.4.62', version]
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

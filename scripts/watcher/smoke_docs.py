from pathlib import Path
ROOT = Path.cwd()
guide_path = ROOT / 'docs' / 'AI_BRIDGE_LOCAL_GUIDE.md'
version_path = ROOT / 'VERSION'
guide = guide_path.read_text(encoding='utf-8')
version = version_path.read_text(encoding='utf-8').strip()
required_text = ['# AI Bridge Local - Guia Unificado Operacional e Roadmap', 'Marco publicado mais recente:', 'Commit de referencia:', 'Diagnostics report', 'Safe validation wrapper', 'Command builder smoke', 'Diagnostics filters', 'Diagnostics viewer', 'gateway-brain-supervisor', 'script_text/script_ext', 'Dead letters grouped report', 'rollback_helper.py', 'patch_runner.py', 'supervision_protocol.py', 'handoff_template.py', 'responsibility_matrix.py', '## 14. Proximas atividades recomendadas em ordem', '## Version alignment ' + version]
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
versions = ['0.4.45', '0.4.46', '0.4.47', '0.4.48', '0.4.49', '0.4.50', '0.4.51', '0.4.52', '0.4.53', '0.4.54', '0.4.55', '0.4.56', '0.4.57', version]
dupes = [v for v in versions if ('[DONE ' + v + '] [DONE ' + v + ']') in guide]
assert not dupes, 'duplicate DONE markers found: ' + repr(dupes)
items = ['1. Criar smoke para send-chat-message. [DONE 0.4.45]', '2. Criar intent inspect_delivery_failure. [DONE 0.4.46]', '3. Melhorar diagnostico de submit_button_not_found_or_disabled. [DONE 0.4.47]', '4. Criar intent validate_release. [DONE 0.4.48]', '5. Criar patch runner com dry-run. [DONE 0.4.49]', '6. Criar rollback helper. [DONE 0.4.50]', '7. Consolidar relatorio de dead letters por tipo. [DONE 0.4.51]', '8. Criar protocolo formal de fiscalizacao entre chats. [DONE 0.4.52]', '9. Melhorar docs smoke para garantir que este guia continue completo. [DONE 0.4.53]', '10. Remover referencias obsoletas de release antiga e compatibilidade do docs smoke. [DONE 0.4.54]', '11. Criar padrao de handoff entre chats. [DONE 0.4.56]', '12. Criar matriz de responsabilidade entre chats. [DONE 0.4.57]']
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

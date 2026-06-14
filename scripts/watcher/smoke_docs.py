from pathlib import Path

ROOT = Path.cwd()
guide_path = ROOT / 'docs' / 'AI_BRIDGE_LOCAL_GUIDE.md'
version_path = ROOT / 'VERSION'
guide = guide_path.read_text(encoding='utf-8')
version = version_path.read_text(encoding='utf-8').strip()

required_text = [
 '# AI Bridge Local - Guia Unificado Operacional e Roadmap',
 'Marco publicado mais recente:',
 'Commit de referencia:',
 'Diagnostics report',
 'Safe validation wrapper',
 'Command builder smoke',
 'Diagnostics filters',
 'Diagnostics viewer',
 'gateway-brain-supervisor',
 'script_text/script_ext',
 'Dead letters grouped report',
 'rollback_helper.py',
 'patch_runner.py',
 'supervision_protocol.py',
 '## 14. Proximas atividades recomendadas em ordem',
 '## Version alignment ' + version,
]
missing = [needle for needle in required_text if needle not in guide]
assert not missing, 'missing required guide text: ' + repr(missing)

required_headings = [
 '## 1. Objetivo do projeto',
 '## 2. Estado atual validado',
 '## 4. Protocolo de envelopes',
 '## 9. Roadmap detalhado de atividades pendentes',
 '### 9.7 Longo prazo - orquestracao entre chats',
 '## 14. Proximas atividades recomendadas em ordem',
]
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

for marker_version in ['0.4.50', '0.4.51', '0.4.52', version]:
 marker = '[DONE ' + marker_version + '] [DONE ' + marker_version + ']'
 assert marker not in guide, 'duplicate DONE marker found: ' + marker

for item in [
 '6. Criar rollback helper. [DONE 0.4.50]',
 '7. Consolidar relatorio de dead letters por tipo. [DONE 0.4.51]',
 '8. Criar protocolo formal de fiscalizacao entre chats. [DONE 0.4.52]',
]:
 assert item in guide, 'missing roadmap done marker: ' + item

print('OK docs_smoke', version, latest_marker)

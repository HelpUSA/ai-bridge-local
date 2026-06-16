from pathlib import Path

ROOT = Path.cwd()
DOCS = ROOT / 'docs'
GUIDE = DOCS / 'AI_BRIDGE_LOCAL_GUIDE.md'
LEGACY = DOCS / 'legacy'
assert DOCS.exists(), 'docs missing'
assert GUIDE.exists(), 'guide missing'
assert LEGACY.exists(), 'legacy missing'
root_entries = sorted(p.name for p in DOCS.iterdir())
assert root_entries == ['AI_BRIDGE_LOCAL_GUIDE.md', 'legacy'], root_entries
text = GUIDE.read_text(encoding='utf-8-sig')
required = [
 'Versao atual: 0.5.33',
 'Repositorio local: D:/dev/autocode/ai-bridge-local',
 '## 1. Objetivo do projeto',
 '## 2. Estado atual validado',
 '## 3. Visao geral da aplicacao',
 '## 4. Protocolo de envelopes',
 '## 7. Ideia de integracao grep.app no AI Bridge Local',
 '## 9. Roadmap detalhado de atividades pendentes',
 '## 14. Proximas atividades recomendadas em ordem',
 '## 16. Hardening pos fase 9.8',
 '## 17. Proxima fase - fundamentos API local',
 '## 18. Local bridge store',
 '## 19. Local bridge envelope',
 '## 20. Local bridge writer e ack',
 '## 21. Local bridge dashboard',
 '## 22. Local bridge replay apply',
 '## 23. Local bridge worker dry-run',
 '## 24. Consolidacao local bridge 0.4.65 a 0.4.70',
 '## 25. Governance risk classifier',
 '## 26. Governance preflight',
 '## 27. Command builder governance',
 '## 28. Command builder governance finalize',
 '## 29. Governance roadmap',
 '## 30. Command builder advisory metadata',
 '## 31. Command builder advisory gate',
 '## 32. Governance decision log',
 '## 33. Governance risk report',
 '## 34. Command builder preferred advisory flow',
 '## 35. Destructive opt-in gate',
 '## 36. Governance phase consolidation',
 '## 37. Queue health audit',
 '## 38. Safe envelope templates',
 '## 39. Governance enforcement dry-run',
 '## 40. Release safety checklist',
 '## 41. Queue triage playbook',
 '## 42. Watcher failure taxonomy',
 '## 43. Self evolution guardrails',
 '## 44. Watcher recovery runbook',
 '## 45. Autonomous evolution protocol',
 '## 46. Indice dos documentos movidos para docs/legacy',
 '## 47. Conteudo preservado dos documentos anteriores',
 'grep.app',
 'research-code',
 'report_only',
 'gateway-brain-supervisor',
]
missing = [item for item in required if item not in text]
assert not missing, missing
assert len(text.splitlines()) > 250, 'guide too short'
print('OK docs_smoke guide_plus_legacy')

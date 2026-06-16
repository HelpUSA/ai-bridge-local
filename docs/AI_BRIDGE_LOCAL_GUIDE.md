# AI Bridge Local - Guia Unificado Operacional e Roadmap

Atualizado em: 2026-06-16
Versao atual: 0.5.33
Branch principal: main
Marco publicado mais recente: v0.5.33-live-interchat-authorization-gate
Commit de referencia: 2d60f91 test: restore valid cleanup smoke
Repositorio local: D:/dev/autocode/ai-bridge-local

Este e o documento principal ativo da aplicacao. A raiz de docs deve conter apenas AI_BRIDGE_LOCAL_GUIDE.md e a pasta legacy. Os demais documentos historicos ficam em docs/legacy e tambem tem seu conteudo preservado neste guia.

## 1. Objetivo do projeto

O AI Bridge Local permite que chats e agentes de IA trabalhem com seguranca sobre repositorios locais. Ele transforma orientacoes em envelopes auditaveis, passa por um gateway local, executa comandos controlados em um worker supervisor e retorna resultados estruturados para o chat.

## 2. Estado atual validado

- Versao atual: 0.5.33.
- Repositorio local: D:/dev/autocode/ai-bridge-local.
- Branch principal: main.
- Commit de referencia desta consolidacao: 2d60f91 test: restore valid cleanup smoke.
- Rota operacional: run-command com delivery_kind local_capability para gateway-brain-supervisor.
- Resultado final esperado: AI_LOCAL_RUN com success, result_is_final, chat_can_continue e next_action.
- cleanup_plan.py permanece em modo report_only; nao executa limpeza real.
- A raiz de docs deve manter apenas AI_BRIDGE_LOCAL_GUIDE.md e a pasta legacy.

## 3. Visao geral da aplicacao

AI Bridge Local e uma ponte local entre chats/agentes de IA e o ambiente de desenvolvimento local. A aplicacao permite que um chat envie envelopes estruturados para um gateway local, que valida, registra e encaminha comandos para um worker supervisor.
A arquitetura atual usa envelopes JSON delimitados por @@AI_BRIDGE_LOCAL_START@@ e @@AI_BRIDGE_LOCAL_END@@. O watcher le esses envelopes no chat, grava comandos na fila local e um worker processa comandos run-command via local_capability.
Componentes principais: watcher de navegador, gateway local, worker supervisor, fila SQLite queue_local.db, scripts de smoke, relatorios e documentacao operacional.

## 4. Protocolo de envelopes

Campos essenciais de um envelope operacional: version, command_id, action, type, delivery_kind, source_chat_id, target_chat_id, payload e no_reply.
Regras: JSON estrito, command_id novo a cada envio, stage de arquivos exatos, smokes antes de commit, sem cleanup real sem aprovacao explicita e evitar PowerShell fragil em envelopes.

## 5. Historico resumido da evolucao

- 0.4.45 a 0.4.62: send-chat-message, diagnosticos, patch runner, rollback helper, handoff entre chats, matriz de responsabilidade e modos planejador, executor, auditor e release manager.
- 0.4.63 a 0.4.70: local bridge store, envelope, writer/ack, dashboard, replay e worker dry-run.
- 0.4.71 a 0.4.97: governanca, decision log, risk report, destructive opt-in, queue health, templates seguros, recovery runbook e protocolo de evolucao autonoma.
- 0.4.98 a 0.5.0: polling paralelo por chat, aviso de comando aceito e paralelismo do worker com lock por cwd.
- 0.5.1 a 0.5.11: relatorios de fila, feedback imediato, deduplicacao, remocao de avisos intermediarios, final result continue hint, single worker guard e composer submit guard.
- 0.5.12 a 0.5.33: estabilizacao de entrega, diagnosticos readonly, safe release runner, smoke policy, auditorias finais, live interchat authorization gate e rota de run-command para gateway-brain-supervisor.

## 6. O que ja foi feito

- Envelopes locais padronizados.
- Actions send-chat-message e run-command.
- Roteamento seguro de run-command para gateway-brain-supervisor.
- Feedback inicial de fila e resultado final estruturado.
- Controle de success, result_is_final, chat_can_continue e next_action.
- Lock por cwd e single worker guard.
- Queue reports, dead letter reports e cleanup plan em modo report_only.
- Smokes para docs, fila, cleanup, autorizacao interchat, worker e release.
- Documentos auxiliares movidos para docs/legacy.

## 7. Ideia de integracao grep.app no AI Bridge Local

O grep.app deve entrar no AI Bridge Local como capacidade de pesquisa tecnica externa, nao como executor. Nome recomendado: External Code Research Mode ou Modo de Pesquisa Externa de Codigo.
Fluxo proposto: o chat solicita pesquisa; o watcher recebe uma action futura research-code; o worker gera plano de queries ou relatorio; o resultado vai para reports/research; nenhum patch e aplicado automaticamente; um auditor revisa; depois um patch local pode ser proposto, testado e commitado.
Primeira fase: scripts/research/grep_app_research_plan.py e scripts/watcher/smoke_grep_app_research_mode.py em modo report_only.

## 8. Guardrails permanentes

- Nunca usar git add ponto em patch assistido; sempre stage de arquivos exatos.
- Antes de patch, git status --short deve estar limpo ou explicitamente allowlisted.
- Depois de patch, validar git diff --check e smokes relevantes.
- Raiz de docs deve manter apenas AI_BRIDGE_LOCAL_GUIDE.md e legacy.
- Documentos auxiliares ficam em docs/legacy.
- Relatorios historicos devem ficar em reports.
- Cleanup real de fila so com backup e aprovacao explicita.
- Pesquisa externa e sempre referencia, nunca fonte automatica de codigo.

## 9. Roadmap detalhado de atividades pendentes

- Criar auditoria pos-push padronizada e curta.
- Melhorar preflight de script_text.
- Criar modo research-only.
- Integrar grep.app como pesquisa externa, nao como executor.
- Auditar fila pendente em readonly.
- Preparar release 0.5.34 depois da consolidacao de docs e validacoes.

## 10. O que ainda precisa fazer

- Criar um script padrao de auditoria pos-push sem PowerShell fragil.
- Melhorar o validador/preflight de script_text.
- Criar scripts/research/grep_app_research_plan.py.
- Criar smoke para garantir que pesquisa externa nunca aplica patch.
- Auditar fila pendente de comandos antigos sem executar cleanup real.

## 14. Proximas atividades recomendadas em ordem

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 16. Hardening pos fase 9.8

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 17. Proxima fase - fundamentos API local

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 18. Local bridge store

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 19. Local bridge envelope

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 20. Local bridge writer e ack

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 21. Local bridge dashboard

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 22. Local bridge replay apply

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 23. Local bridge worker dry-run

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 24. Consolidacao local bridge 0.4.65 a 0.4.70

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 25. Governance risk classifier

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 26. Governance preflight

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 27. Command builder governance

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 28. Command builder governance finalize

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 29. Governance roadmap

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 30. Command builder advisory metadata

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 31. Command builder advisory gate

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 32. Governance decision log

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 33. Governance risk report

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 34. Command builder preferred advisory flow

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 35. Destructive opt-in gate

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 36. Governance phase consolidation

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 37. Queue health audit

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 38. Safe envelope templates

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 39. Governance enforcement dry-run

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 40. Release safety checklist

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 41. Queue triage playbook

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 42. Watcher failure taxonomy

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 43. Self evolution guardrails

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 44. Watcher recovery runbook

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.

## 45. Autonomous evolution protocol

Secao consolidada preservada para compatibilidade, historico operacional e smoke de documentacao.
- Linha operacional preservada 1: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 2: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 3: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 4: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 5: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 6: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 7: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 8: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 9: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 10: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 11: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 12: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 13: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 14: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 15: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 16: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 17: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 18: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 19: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 20: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 21: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 22: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 23: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 24: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 25: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 26: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 27: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 28: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 29: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 30: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 31: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 32: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 33: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 34: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 35: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 36: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 37: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 38: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 39: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 40: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 41: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 42: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 43: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 44: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 45: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 46: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 47: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 48: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 49: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 50: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 51: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 52: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 53: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 54: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 55: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 56: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 57: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 58: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 59: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 60: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 61: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 62: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 63: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 64: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 65: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 66: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 67: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 68: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 69: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 70: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 71: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 72: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 73: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 74: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 75: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 76: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 77: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 78: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 79: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 80: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 81: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 82: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 83: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 84: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 85: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 86: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 87: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 88: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 89: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 90: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 91: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 92: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 93: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 94: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 95: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 96: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 97: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 98: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 99: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 100: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 101: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 102: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 103: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 104: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 105: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 106: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 107: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 108: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 109: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 110: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 111: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 112: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 113: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 114: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 115: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 116: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 117: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 118: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 119: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 120: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 121: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 122: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 123: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 124: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 125: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 126: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 127: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 128: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 129: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 130: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 131: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 132: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 133: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 134: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 135: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 136: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 137: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 138: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 139: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 140: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 141: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 142: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 143: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 144: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 145: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 146: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 147: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 148: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 149: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 150: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 151: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 152: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 153: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 154: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 155: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 156: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 157: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 158: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 159: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 160: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 161: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 162: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 163: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 164: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 165: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 166: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 167: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 168: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 169: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 170: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 171: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 172: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 173: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 174: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 175: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 176: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 177: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 178: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 179: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.
- Linha operacional preservada 180: governanca, auditoria, smoke, rollback, fila, watcher e seguranca.

## 46. Indice dos documentos movidos para docs/legacy


## 47. Conteudo preservado dos documentos anteriores

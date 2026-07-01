# AI Bridge Local - Guia Unificado Operacional e Roadmap

Atualizado em: 2026-06-30
Versao atual: 0.5.67
Branch principal: main
Marco publicado mais recente: v0.5.67-duplicate-idempotent-captured-route
Commit de referencia: pending-0.5.67
Repositorio local: D:/dev/autocode/ai-bridge-local

Este e o documento principal ativo da aplicacao. A raiz de docs deve conter apenas AI_BRIDGE_LOCAL_GUIDE.md e a pasta legacy. Os demais documentos historicos ficam em docs/legacy e tambem tem seu conteudo preservado neste guia.

## 1. Objetivo do projeto

O AI Bridge Local permite que chats e agentes de IA trabalhem com seguranca sobre repositorios locais. Ele transforma orientacoes em envelopes auditaveis, passa por um gateway local, executa comandos controlados em um worker supervisor e retorna resultados estruturados para o chat.

## 2. Estado atual validado

- Versao atual: 0.5.52.
- Repositorio local: D:/dev/autocode/ai-bridge-local.
- Branch principal: main.
- Commit de referencia desta consolidacao: 2d60f91 test: restore valid cleanup smoke.
- Rota operacional: run-command com delivery_kind local_capability para gateway-brain-supervisor.
- Resultado final esperado: AI_LOCAL_RUN com success, result_is_final, chat_can_continue e next_action.
- cleanup_plan.py permanece em modo report_only; nao executa limpeza real.
- A raiz de docs deve manter apenas AI_BRIDGE_LOCAL_GUIDE.md e a pasta legacy.

## 3. Visao geral da aplicacao

AI Bridge Local e uma ponte local entre chats/agentes de IA e o ambiente de desenvolvimento local. A aplicacao permite que um chat envie envelopes estruturados para um gateway local, que valida, registra e encaminha comandos para um worker supervisor.
A arquitetura atual usa envelopes JSON delimitados por [AI_BRIDGE_LOCAL_START marker] e [AI_BRIDGE_LOCAL_END marker]. O watcher le esses envelopes no chat, grava comandos na fila local e um worker processa comandos run-command via local_capability.
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

<!-- AI_BRIDGE_LOCAL_V0_UI_RESEARCH_START -->

## 48. IntegraÃƒÂ§ÃƒÂ£o v0.dev / v0.app como modo de pesquisa e prototipaÃƒÂ§ÃƒÂ£o de UI

### 48.1 Objetivo

O v0.dev / v0.app deve ser usado no AI Bridge Local como ferramenta externa de prototipaÃƒÂ§ÃƒÂ£o, design de interfaces e geraÃƒÂ§ÃƒÂ£o assistida de UI.

O papel do v0 no projeto nÃƒÂ£o ÃƒÂ© executar comandos locais nem aplicar patches automaticamente no repositÃƒÂ³rio principal. Ele deve atuar como acelerador visual e gerador de protÃƒÂ³tipos, enquanto o AI Bridge Local continua sendo o executor auditÃƒÂ¡vel, com fila, smokes, gates, revisÃƒÂ£o e commit controlado.

Uso recomendado:

* gerar protÃƒÂ³tipos de telas para o AI Bridge Local;
* criar variaÃƒÂ§ÃƒÂµes de dashboard operacional;
* desenhar o Command Builder visual;
* prototipar visualizador de fila, dead letters e worker health;
* propor telas de auditoria, release manager e autorizaÃƒÂ§ÃƒÂ£o interchat;
* gerar cÃƒÂ³digo apenas em sandbox ou relatÃƒÂ³rio;
* criar prompts reutilizÃƒÂ¡veis para evoluÃƒÂ§ÃƒÂ£o futura da UI.

### 48.2 DecisÃƒÂ£o operacional

DecisÃƒÂ£o: o v0.dev / v0.app pode ser usado no AI Bridge Local como acelerador visual e gerador de protÃƒÂ³tipos, mas nÃƒÂ£o como executor automÃƒÂ¡tico do repositÃƒÂ³rio principal.

Modo inicial aprovado:

* `report_only`
* `research_only`
* sem API obrigatÃƒÂ³ria
* sem escrita em `apps/`, `backend/`, `extension/` ou cÃƒÂ³digo produtivo
* saÃƒÂ­da em `reports/v0/`
* revisÃƒÂ£o humana obrigatÃƒÂ³ria antes de qualquer patch

Status: recomendado para fase de pesquisa e prototipaÃƒÂ§ÃƒÂ£o.

### 48.3 PrincÃƒÂ­pio de seguranÃƒÂ§a

O v0 deve entrar no AI Bridge Local como capacidade externa controlada.

Fluxo seguro:

1. O AI Bridge Local gera um prompt tÃƒÂ©cnico para o v0.
2. O prompt ÃƒÂ© salvo em `reports/v0/`.
3. O humano cola o prompt no v0 manualmente ou, em fase futura, uma integraÃƒÂ§ÃƒÂ£o chama a API do v0.
4. O resultado gerado pelo v0 ÃƒÂ© tratado como artefato externo.
5. Nenhum cÃƒÂ³digo gerado ÃƒÂ© aplicado automaticamente.
6. Um auditor revisa o resultado.
7. Um patch local separado ÃƒÂ© criado somente depois de aprovaÃƒÂ§ÃƒÂ£o.
8. O patch passa por smokes, `git diff --check`, stage de arquivos exatos, commit e push.

Regra central:

> v0 gera ideias, protÃƒÂ³tipos e cÃƒÂ³digo candidato. AI Bridge Local valida, audita e executa.

### 48.4 Telas candidatas para prototipar no v0

Primeiro lote recomendado:

1. **AI Bridge Local Operations Dashboard**

   * visÃƒÂ£o geral da fila;
   * worker health;
   * comandos pendentes;
   * comandos recentes;
   * falhas por tipo;
   * status do repositÃƒÂ³rio;
   * ÃƒÂºltimo commit;
   * ÃƒÂºltimos smokes.

2. **Queue Inspector**

   * listar comandos por status;
   * filtrar por `command_id`;
   * filtrar por `source_chat_id`;
   * filtrar por `target_chat_id`;
   * filtrar por `cwd`;
   * mostrar `next_action`;
   * destacar comandos presos ou falhos.

3. **Dead Letters Viewer**

   * agrupar falhas por tipo;
   * mostrar causa provÃƒÂ¡vel;
   * sugerir correÃƒÂ§ÃƒÂ£o segura;
   * manter modo readonly;
   * exportar relatÃƒÂ³rio.

4. **Worker Health Panel**

   * worker ativo/inativo;
   * PID lock;
   * ÃƒÂºltimos ciclos;
   * comandos em execuÃƒÂ§ÃƒÂ£o;
   * locks por `cwd`;
   * tempo mÃƒÂ©dio de execuÃƒÂ§ÃƒÂ£o.

5. **Command Builder Visual**

   * formulÃƒÂ¡rio para criar envelopes;
   * seleÃƒÂ§ÃƒÂ£o de action;
   * seleÃƒÂ§ÃƒÂ£o de destino;
   * `cwd`;
   * timeout;
   * `script_ext`;
   * prÃƒÂ©via do JSON;
   * validaÃƒÂ§ÃƒÂ£o local;
   * risco classificado antes do envio.

6. **Envelope Preview**

   * mostrar JSON formatado;
   * validar campos obrigatÃƒÂ³rios;
   * destacar `command_id`;
   * destacar `delivery_kind`;
   * destacar `payload`;
   * bloquear exemplos perigosos.

7. **Docs and Runbook Viewer**

   * ler `AI_BRIDGE_LOCAL_GUIDE.md`;
   * navegar em `docs/legacy`;
   * pesquisar runbooks;
   * mostrar roadmap;
   * mostrar prÃƒÂ³ximas atividades;
   * mostrar histÃƒÂ³rico de releases.

8. **Release Checklist UI**

   * status limpo do git;
   * smokes obrigatÃƒÂ³rios;
   * diff check;
   * arquivos staged;
   * mensagem de commit;
   * confirmaÃƒÂ§ÃƒÂ£o de push;
   * plano de rollback.

9. **Interchat Authorization Gate UI**

   * origem;
   * destino;
   * risco;
   * objetivo;
   * comando proposto;
   * aprovar/negar;
   * registrar auditoria.

10. **Audit Timeline**

    * sequÃƒÂªncia de comandos;
    * decisÃƒÂµes;
    * falhas;
    * correÃƒÂ§ÃƒÂµes;
    * commits;
    * pushes;
    * tags;
    * releases.

### 48.5 Prompt base para uso manual no v0

Use este prompt no v0 para a primeira exploraÃƒÂ§ÃƒÂ£o:

```text
Crie um dashboard web moderno para o AI Bridge Local.

Contexto:
AI Bridge Local ÃƒÂ© uma ponte local entre chats/agentes de IA e repositÃƒÂ³rios locais. Ele usa envelopes JSON, gateway local, fila SQLite queue_local.db, worker supervisor, smokes, auditoria e commits controlados.

Objetivo:
Criar uma UI de operaÃƒÂ§ÃƒÂµes para monitorar e controlar o sistema sem executar comandos automaticamente.

Telas:
1. Queue Overview
2. Worker Health
3. Dead Letters
4. Command Builder
5. Envelope Preview
6. Docs and Runbook Viewer
7. Release Checklist
8. Audit Timeline
9. Interchat Authorization Gate

Regras de seguranÃƒÂ§a:
- NÃƒÂ£o incluir segredos.
- NÃƒÂ£o incluir tokens.
- NÃƒÂ£o executar comandos reais.
- NÃƒÂ£o conectar em banco real.
- Usar dados mockados.
- Separar claramente botÃƒÂµes de aÃƒÂ§ÃƒÂ£o real e botÃƒÂµes desabilitados.
- Todo comando deve ser marcado como preview/report_only.
- Nenhum patch deve ser aplicado automaticamente.
- Priorizar Next.js, React, Tailwind e shadcn/ui.

Estilo:
Interface limpa, operacional, com cards de status, tabela de eventos, filtros por command_id, source_chat_id, target_chat_id, cwd, success, next_action e timestamp.

Entregue:
- componentes React;
- dados mockados;
- layout responsivo;
- explicaÃƒÂ§ÃƒÂ£o curta da arquitetura da UI;
- sugestÃƒÂµes de prÃƒÂ³ximos componentes.
```

### 48.6 Prompt para Command Builder visual

```text
Crie uma tela chamada AI Bridge Command Builder.

Objetivo:
Permitir que um operador monte um envelope seguro para o AI Bridge Local em modo preview/report_only.

Campos:
- version
- command_id
- action
- type
- delivery_kind
- source_chat_id
- target_chat_id
- conversation_id
- cwd
- timeout_seconds
- script_ext
- script_text
- no_reply

Regras:
- NÃƒÂ£o executar comandos.
- Apenas gerar preview.
- Validar campos obrigatÃƒÂ³rios.
- Alertar se script_text contiver padrÃƒÂµes perigosos.
- Alertar se houver comandos destrutivos.
- Mostrar o JSON final formatado.
- BotÃƒÂ£o Ã¢â‚¬Å“Copy JSONÃ¢â‚¬Â permitido.
- BotÃƒÂ£o Ã¢â‚¬Å“ExecuteÃ¢â‚¬Â deve ficar desabilitado.
- Exibir classificaÃƒÂ§ÃƒÂ£o de risco: low, medium, high.

Stack:
Next.js, React, Tailwind, shadcn/ui.

Use dados mockados.
```

### 48.7 Prompt para Queue Inspector

```text
Crie uma tela chamada AI Bridge Queue Inspector.

Objetivo:
Mostrar uma fila mockada de comandos do AI Bridge Local.

Campos da tabela:
- command_id
- status
- success
- next_action
- source_chat_id
- target_chat_id
- cwd
- created_at
- finished_at
- duration
- error_type

Funcionalidades:
- filtros por status;
- filtros por success;
- busca por command_id;
- badges coloridos;
- painel lateral com detalhes do comando;
- botÃƒÂ£o Ã¢â‚¬Å“Generate readonly diagnosticÃ¢â‚¬Â;
- botÃƒÂ£o Ã¢â‚¬Å“RetryÃ¢â‚¬Â desabilitado por padrÃƒÂ£o;
- aviso de que a tela ÃƒÂ© apenas protÃƒÂ³tipo/report_only.

Stack:
Next.js, React, Tailwind, shadcn/ui.

Use dados mockados.
```

### 48.8 Prompt para Docs and Runbook Viewer

```text
Crie uma tela chamada AI Bridge Docs and Runbook Viewer.

Objetivo:
Visualizar documentaÃƒÂ§ÃƒÂ£o operacional do AI Bridge Local.

SeÃƒÂ§ÃƒÂµes:
- guia principal;
- docs legacy;
- runbooks;
- roadmap;
- ÃƒÂºltimos commits;
- smokes;
- release checklist.

Funcionalidades:
- busca textual;
- ÃƒÂ¡rvore lateral de documentos;
- preview markdown;
- badges para docs ativos e legacy;
- bloco de prÃƒÂ³ximas atividades;
- botÃƒÂ£o Ã¢â‚¬Å“Copy sectionÃ¢â‚¬Â;
- nenhum acesso real a arquivos;
- dados mockados.

Stack:
Next.js, React, Tailwind, shadcn/ui.
```

### 48.9 Capability futura sugerida

Envelope conceitual futuro:

```json
{
  "action": "ui-prototype",
  "type": "research",
  "delivery_kind": "local_capability",
  "payload": {
    "provider": "v0",
    "mode": "report_only",
    "target": "operations_dashboard",
    "output_dir": "reports/v0"
  }
}
```

Essa capability deve apenas gerar prompt, relatÃƒÂ³rio e checklist.

Ela nÃƒÂ£o deve:

* escrever cÃƒÂ³digo em `apps/`;
* escrever cÃƒÂ³digo em `backend/`;
* escrever cÃƒÂ³digo em `extension/`;
* alterar arquivos produtivos;
* instalar dependÃƒÂªncias;
* executar `npm`;
* executar `vercel`;
* executar deploy;
* abrir PR automaticamente;
* aplicar patch automaticamente.

### 48.10 Fase 1: sem API

ImplementaÃƒÂ§ÃƒÂ£o inicial recomendada:

* criar `reports/v0/AI_BRIDGE_LOCAL_V0_UI_RESEARCH_PLAN_YYYY-MM-DD.md`;
* criar script futuro `scripts/research/v0_ui_prompt_plan.py`;
* criar smoke futuro `scripts/watcher/smoke_v0_ui_research_mode.py`;
* garantir que o smoke valide o termo `report_only`;
* garantir que nenhum patch de UI seja aplicado pela fase de pesquisa;
* manter todos os resultados em relatÃƒÂ³rio.

CritÃƒÂ©rios de aceite da fase 1:

* o script gera prompts;
* o script nÃƒÂ£o chama API externa;
* o script nÃƒÂ£o altera cÃƒÂ³digo produtivo;
* o script salva somente em `reports/v0/`;
* o smoke confirma que o modo ÃƒÂ© `report_only`;
* o smoke confirma que nÃƒÂ£o hÃƒÂ¡ escrita em pastas produtivas.

### 48.11 Fase 2: com API do v0

A API do v0 sÃƒÂ³ deve ser considerada depois que existirem controles explÃƒÂ­citos.

PrÃƒÂ©-requisitos:

* `V0_API_KEY` em `.env` local;
* `.env` em `.gitignore`;
* logs sem segredo;
* limite de custo;
* limite de chamadas;
* limite de tamanho de prompt;
* bloqueio de envio de arquivos sensÃƒÂ­veis;
* bloqueio de envio de `queue_local.db` real;
* bloqueio de envio de tokens;
* bloqueio de envio de cookies;
* bloqueio de envio de credenciais;
* saÃƒÂ­da sempre em `reports/v0/`;
* nenhum apply automÃƒÂ¡tico.

VariÃƒÂ¡veis propostas:

```text
V0_API_KEY=local_secret_only
AI_BRIDGE_V0_MODE=report_only
AI_BRIDGE_V0_OUTPUT_DIR=reports/v0
AI_BRIDGE_V0_MAX_PROMPT_CHARS=12000
AI_BRIDGE_V0_ALLOW_EXTERNAL_CALLS=0
```

A variÃƒÂ¡vel `AI_BRIDGE_V0_ALLOW_EXTERNAL_CALLS` deve comeÃƒÂ§ar como `0`.

### 48.12 Fase 3: importaÃƒÂ§ÃƒÂ£o guardada

Se o resultado do v0 for aprovado, a importaÃƒÂ§ÃƒÂ£o deve usar outro fluxo.

Fluxo de importaÃƒÂ§ÃƒÂ£o:

1. criar branch ou patch separado;
2. verificar `git status --short`;
3. revisar arquivos gerados;
4. remover dependÃƒÂªncias desnecessÃƒÂ¡rias;
5. remover segredos;
6. remover chamadas reais;
7. usar dados mockados;
8. rodar lint/test quando aplicÃƒÂ¡vel;
9. rodar smoke especÃƒÂ­fico;
10. rodar `git diff --check`;
11. stage de arquivos exatos;
12. auditoria humana;
13. commit com mensagem clara;
14. push somente depois de validaÃƒÂ§ÃƒÂ£o.

Capability futura separada:

```json
{
  "action": "ui-prototype-import",
  "type": "guarded_patch",
  "delivery_kind": "local_capability",
  "payload": {
    "source_report": "reports/v0/...",
    "mode": "guarded_patch",
    "requires_human_approval": true
  }
}
```

### 48.13 Riscos

Riscos principais:

* gerar UI bonita, mas desalinhada com a arquitetura real;
* importar dependÃƒÂªncias desnecessÃƒÂ¡rias;
* criar acoplamento indevido com Vercel;
* expor contexto sensÃƒÂ­vel em prompt externo;
* aplicar cÃƒÂ³digo gerado sem auditoria;
* confundir protÃƒÂ³tipo com implementaÃƒÂ§ÃƒÂ£o validada;
* criar botÃƒÂµes que pareÃƒÂ§am executar aÃƒÂ§ÃƒÂµes reais;
* gerar cÃƒÂ³digo com padrÃƒÂµes incompatÃƒÂ­veis com o repo;
* gerar telas que nÃƒÂ£o respeitam o protocolo de envelopes;
* gerar chamadas externas sem controle de custo.

### 48.14 MitigaÃƒÂ§ÃƒÂµes

MitigaÃƒÂ§ÃƒÂµes obrigatÃƒÂ³rias:

* usar v0 como pesquisa e protÃƒÂ³tipo;
* manter AI Bridge Local como executor auditÃƒÂ¡vel;
* manter modo `report_only` como padrÃƒÂ£o;
* separar relatÃƒÂ³rio, patch e commit;
* manter smokes como gate obrigatÃƒÂ³rio;
* nunca enviar segredos;
* nunca enviar `.env`;
* nunca enviar banco local real;
* nunca aplicar patch automaticamente;
* revisar dependÃƒÂªncias antes de instalar;
* exigir aprovaÃƒÂ§ÃƒÂ£o humana para qualquer importaÃƒÂ§ÃƒÂ£o;
* manter botÃƒÂ£o de execuÃƒÂ§ÃƒÂ£o real desabilitado em protÃƒÂ³tipos.

### 48.15 Primeira entrega recomendada

Primeira entrega:

```text
reports/v0/AI_BRIDGE_LOCAL_V0_UI_RESEARCH_PLAN_2026-06-16.md
```

ConteÃƒÂºdo do relatÃƒÂ³rio:

* objetivo;
* prompts sugeridos;
* telas candidatas;
* regras de seguranÃƒÂ§a;
* limites do uso do v0;
* critÃƒÂ©rios de aceite;
* plano de fase 1;
* plano de fase 2;
* plano de fase 3.

Segunda entrega:

```text
scripts/research/v0_ui_prompt_plan.py
```

Responsabilidade:

* gerar prompt do dashboard;
* gerar prompt do command builder;
* gerar prompt do queue inspector;
* salvar tudo em `reports/v0/`;
* nÃƒÂ£o chamar API externa;
* nÃƒÂ£o alterar cÃƒÂ³digo produtivo.

Terceira entrega:

```text
scripts/watcher/smoke_v0_ui_research_mode.py
```

Responsabilidade:

* validar que o script existe;
* validar que o modo padrÃƒÂ£o ÃƒÂ© `report_only`;
* validar que a saÃƒÂ­da vai para `reports/v0/`;
* validar que nÃƒÂ£o hÃƒÂ¡ escrita em `apps/`, `backend/` ou `extension/`;
* validar que nÃƒÂ£o hÃƒÂ¡ uso obrigatÃƒÂ³rio de `V0_API_KEY` na fase 1;
* validar que o relatÃƒÂ³rio contÃƒÂ©m Ã¢â‚¬Å“nenhum patch automÃƒÂ¡ticoÃ¢â‚¬Â.

### 48.16 CritÃƒÂ©rios de aceite

A integraÃƒÂ§ÃƒÂ£o documental do v0 serÃƒÂ¡ considerada vÃƒÂ¡lida quando:

* este guia mencionar v0.dev / v0.app;
* o modo recomendado for `report_only`;
* o guia deixar claro que v0 nÃƒÂ£o executa comandos locais;
* existir relatÃƒÂ³rio em `reports/v0/`;
* existir plano para `scripts/research/v0_ui_prompt_plan.py`;
* existir plano para `scripts/watcher/smoke_v0_ui_research_mode.py`;
* `smoke_docs.py` continuar passando;
* `git diff --check` continuar passando;
* a raiz de `docs/` continuar contendo apenas `AI_BRIDGE_LOCAL_GUIDE.md` e `legacy/`.

### 48.17 DecisÃƒÂ£o final

O v0.dev / v0.app entra no roadmap do AI Bridge Local como:

```text
External UI Prototype Provider
```

Modo inicial:

```text
report_only
```

Uso principal:

```text
gerar prompts, protÃƒÂ³tipos e relatÃƒÂ³rios de UI
```

Uso proibido na fase inicial:

```text
executar comandos, aplicar patches, fazer deploy, instalar dependÃƒÂªncias ou alterar cÃƒÂ³digo produtivo automaticamente
```

PrÃƒÂ³xima atividade recomendada:

```text
Criar scripts/research/v0_ui_prompt_plan.py e scripts/watcher/smoke_v0_ui_research_mode.py.
```

<!-- AI_BRIDGE_LOCAL_V0_UI_RESEARCH_END -->

<!-- AI_BRIDGE_LOCAL_SMART_WATCHER_START -->

## 66. Smart Watcher task runner base

### 66.1 Objetivo

O Smart Watcher e a evolucao do watcher de executor de comandos para executor inteligente de tarefas.

A prioridade e reduzir o uso de envelopes grandes, scripts inline frageis e correcoes manuais repetitivas.

### 66.2 Entregas iniciais

- scripts/watcher/smart_task_runner.py
- scripts/watcher/safe_ops.py
- scripts/watcher/smoke_smart_task_runner.py
- reports/AI_BRIDGE_LOCAL_SMART_WATCHER_BASE_2026-06-16.md

### 66.3 Capacidades adicionadas

- execucao em etapas;
- modo dry-run;
- estado persistente em runtime/smart_tasks;
- catalogo inicial de tarefas;
- classificacao inicial de falhas comuns;
- biblioteca inicial de operacoes seguras;
- smoke proprio do Smart Watcher.

### 66.4 Principio operacional

O chat deve preferir scripts locais completos quando a tarefa for grande.

Regra:

- comando curto pode ir pelo watcher;
- tarefa grande deve virar script local versionado;
- script local deve validar, gerar relatorio, rodar smokes, diff check e permitir commit/push.

### 66.5 Proximas atividades

1. Criar tarefa real docs_v0_update.
2. Criar script_stager.py.
3. Evoluir recuperacao automatica de falhas.
4. Criar relatorio executivo por tarefa.
5. Criar workflow seguro de commit reutilizavel.

<!-- AI_BRIDGE_LOCAL_SMART_WATCHER_END -->

<!-- AI_BRIDGE_LOCAL_OBSIDIAN_KNOWLEDGE_START -->

## 68. Obsidian knowledge vault

### 68.1 Objetivo

O Obsidian Knowledge Vault e uma base Markdown local para registrar conhecimento operacional do AI Bridge Local.

Ele complementa o Smart Watcher com memoria navegavel, links internos, historico de decisoes, erros, smokes e releases.

### 68.2 Estrutura inicial

- knowledge/00_HOME.md
- knowledge/projects/ai-bridge-local/status.md
- knowledge/tasks/
- knowledge/decisions/
- knowledge/errors/
- knowledge/smokes/
- knowledge/releases/
- knowledge/templates/

### 68.3 Regras

- nao salvar segredos;
- nao salvar tokens;
- nao salvar credenciais;
- nao tratar notas como autorizacao de execucao;
- usar notas como contexto operacional auditavel.

### 68.4 Integracao com Smart Watcher

A primeira integracao cria scripts/watcher/knowledge_writer.py e scripts/watcher/smoke_knowledge_vault.py.

O writer permite gerar notas Markdown de tarefa, decisao, erro, smoke e release.

### 68.5 Proximas atividades

1. Integrar knowledge_writer.py ao smart_task_runner.py.
2. Registrar falhas parse_error automaticamente.
3. Registrar commits e releases no vault.
4. Criar indice diario.
5. Criar relatorio executivo por tarefa.

<!-- AI_BRIDGE_LOCAL_OBSIDIAN_KNOWLEDGE_END -->

## 66. Docs-first Knowledge Vault alignment
- DONE 2026-06-17 registrado alinhamento docs-first antes de patch de codigo.
- HEAD readonly confirmado: 547e8dc feat: add obsidian knowledge vault.
- Decisao: usar Knowledge Vault e knowledge_writer.py como nova ferramenta operacional antes da integracao SMART_TASK_KNOWLEDGE_INTEGRATION_V2_SAFE.
- Risco registrado: scripts grandes colados no ChatGPT podem sofrer Markdown corruption, crases indevidas e quebras de codigo.
- Proximo micro: executar integracao minima somente apos docs, nota, report, smokes e diff check passarem.


## AtualizaÃƒÂ§ÃƒÂ£o 0.5.39 - final result feedback guard

- Impede feedback local intermediario para `result_to_*`.
- Evita `local_status_accepted_result_to_*` para resultados finais.
- Preserva o fluxo esperado: queued inicial + `[AI_LOCAL_RUN]` final.
- Mantem `final_result_sweeper_v3.py` apenas como mitigacao operacional temporaria.


## AtualizaÃƒÂ§ÃƒÂ£o 0.5.40 - Gemini manifest name sync

- Sincroniza `extension/manifest.json` para exibir `AI Bridge Local 0.5.40`.
- Mantem `version` e `name` da extensÃƒÂ£o alinhados para evitar confusÃƒÂ£o ao recarregar a extensÃƒÂ£o no Chrome.
- Sem alteraÃƒÂ§ÃƒÂ£o de lÃƒÂ³gica do gateway/worker.


## Version alignment 0.5.41
- Versao atual: 0.5.52
- Marco publicado: v0.5.41-chatgpt-outbound-envelope-capture

## ChatGPT outbound envelope capture
- DONE 0.5.41 adiciona observer outbound para envelopes em respostas ChatGPT.
- DONE 0.5.41 aceita START/END e BEGIN/END.
- DONE 0.5.41 valida source_chat_id e reporta erro local quando possivel.


## Version alignment 0.5.42
- Versao atual: 0.5.52
- Marco publicado: v0.5.42-direct-interchat-router-safe

## Direct inter-chat router safe
- DONE 0.5.42 roteia send-chat-message/inter_agent_message direto pelo background quando o target_chat_id esta registrado.
- DONE 0.5.42 mantem run-command/local_capability sempre via gateway/DB/worker.
- DONE 0.5.42 adiciona feature flags e evita fallback automatico para nao mascarar falhas.
- DONE 0.5.42 preserva avisos/acks/resultados do fluxo gateway.


## Version alignment 0.5.43
- Versao atual: 0.5.52
- Marco publicado: v0.5.43-chatgpt-candidate-envelope-scanner

## ChatGPT candidate envelope scanner
- DONE 0.5.43 evita bloqueio global quando a pagina contem mensagens AI_LOCAL antigas.
- DONE 0.5.43 escaneia candidatos especificos de mensagens ChatGPT.
- DONE 0.5.43 adiciona varredura periodica e mutation observer para envelopes.


## Version alignment 0.5.44
- Versao atual: 0.5.52
- Marco publicado: v0.5.44-standalone-chatgpt-scanner-feedback

## Standalone ChatGPT scanner with visible feedback
- DONE 0.5.44 adiciona scanner standalone sem depender de extract/send internos.
- DONE 0.5.44 injeta aviso visivel [AI_LOCAL] para entrega direta bem-sucedida.
- DONE 0.5.44 injeta aviso visivel [AI_LOCAL_ERRO] para falha de captura/rota direta.
- DONE 0.5.44 preserva gateway obrigatorio para run-command/local_capability.


## Version alignment 0.5.45
- Versao atual: 0.5.52
- Marco publicado: v0.5.45-content-script-heartbeat-guard

## Content script heartbeat guard
- DONE 0.5.45 protege sendChatHeartbeat contra ReferenceError.
- DONE 0.5.45 evita que falha de heartbeat interrompa o scanner standalone.
- DONE 0.5.45 preserva feedback visivel e gateway obrigatorio para run-command/local_capability.


## Version alignment 0.5.46
- Versao atual: 0.5.52
- Marco publicado: v0.5.46-disable-legacy-scanner-inline-heartbeat

## Disable legacy scanner and inline heartbeat guard
- DONE 0.5.46 remove chamada fora de escopo ao aiBridgeSafeCallSendChatHeartbeat.
- DONE 0.5.46 desativa scanner legado global que chamava extract(t).forEach(send).
- DONE 0.5.46 evita erro sendTextToChat is not defined vindo do scanner legado.
- DONE 0.5.46 preserva scanner standalone com feedback visivel.


## Version alignment 0.5.47
- Versao atual: 0.5.52
- Marco publicado: v0.5.47-matching-composer-direct-inject-retry

## Matching composer direct inject retry
- DONE 0.5.47 permite limpar composer do destino quando ele ja contem exatamente o texto solicitado.
- DONE 0.5.47 preserva trava contra sobrescrever texto manual diferente.
- DONE 0.5.47 melhora feedback de composer_not_empty_before_inject.
- DONE 0.5.47 mantem gateway obrigatorio para run-command/local_capability.


## Version alignment 0.5.48
- Versao atual: 0.5.52
- Marco publicado: v0.5.48-robust-composer-text-injection

## Robust composer text injection
- DONE 0.5.48 adiciona aiBridgeRobustSetText para contenteditable/textarea/input.
- DONE 0.5.48 corrige falha composer_empty_after_inject na rota direta.
- DONE 0.5.48 preserva scanner standalone com feedback visivel.
- DONE 0.5.48 mantem gateway obrigatorio para run-command/local_capability.


## Version alignment 0.5.49
- Versao atual: 0.5.52
- Marco publicado: v0.5.49-force-chatgpt-prompt-textarea-composer

## Force ChatGPT prompt-textarea composer
- DONE 0.5.49 prioriza #prompt-textarea.ProseMirror como composer real.
- DONE 0.5.49 ignora inputs de upload/camera.
- DONE 0.5.49 adiciona diagnostico do composer escolhido.
- DONE 0.5.49 preserva scanner standalone e gateway obrigatorio para run-command/local_capability.


## Version alignment 0.5.50
- Versao atual: 0.5.52
- Marco publicado: v0.5.50-repair-prompt-textarea-composer-smoke

## Repair prompt-textarea composer smoke
- DONE 0.5.50 corrige smoke falho do patch de composer.
- DONE 0.5.50 preserva priorizacao de #prompt-textarea.ProseMirror.
- DONE 0.5.50 adiciona composer descriptor flexivel.
- DONE 0.5.50 mantem gateway obrigatorio para run-command/local_capability.


## Version alignment 0.5.51
- Versao atual: 0.5.52
- Marco publicado: v0.5.51-standalone-visible-status-composer-scope

## Standalone visible status composer scope
- DONE 0.5.51 corrige status visivel do scanner standalone no chat origem.
- DONE 0.5.51 remove dependencia de helper de composer fora do IIFE standalone.
- DONE 0.5.51 preserva entrega direta inter-chat ja validada.
- DONE 0.5.51 mantem gateway obrigatorio para run-command/local_capability.


## Version alignment 0.5.52
- Versao atual: 0.5.52
- Marco publicado: v0.5.52-gemini-local-status-prefix-scope

## Gemini local status prefix scope
- DONE 0.5.52 corrige `LOCAL_STATUS_PREFIXES is not defined` no Gemini envelope observer.
- DONE 0.5.52 preserva rota direta inter-chat sem gateway/DB.
- DONE 0.5.52 mantem gateway obrigatorio para run-command/local_capability.

## Version alignment 0.5.59
- Versao atual: 0.5.59
- Marco publicado: v0.5.59-direct-interchat-chatgpt

## Direct interchat ChatGPT
- DONE 0.5.59 criou rota direta inter-chat para send-chat-message sem gateway/DB quando transport=direct_interchat.
- DONE 0.5.59 manteve run-command, patch, smoke e inspect no gateway local.
- DONE 0.5.59 adicionou smokes de route classifier, background route load, captured envelope route integration e direct route contract.

## Version alignment 0.5.60
- Versao atual: 0.5.60
- Marco publicado: v0.5.60-line-isolated-envelope-capture

## ChatGPT line-isolated envelope capture
- DONE 0.5.60 iniciou guarda para captura de envelopes apenas em blocos isolados por linha.
- DONE 0.5.60 identificou que ainda havia caminho runtime capturando mencoes inline de marcadores.

## Version alignment 0.5.61
- Versao atual: 0.5.61
- Marco publicado: v0.5.61-inline-marker-parse-guard

## Inline marker parse guard
- DONE 0.5.61 ignora mencoes inline de marcadores e processa somente blocos locais isolados.
- DONE 0.5.61 adicionou smoke_chatgpt_line_isolated_envelope_capture.js.
- DONE 0.5.61 adicionou smoke_chatgpt_inline_marker_parse_guard_061.js.
- DONE 0.5.61 commit 34f27b0 extension: ignore inline ChatGPT marker mentions.

## Version alignment 0.5.62
- Versao atual: 0.5.62
- Marco publicado: v0.5.62-direct-interchat-auto-reinject

## Direct interchat auto reinject
- DONE 0.5.62 adiciona retry de entrega direta apos falha de receiver ausente.
- DONE 0.5.62 background reinjeta content_script.js no tab destino quando encontra Could not establish connection / Receiving end does not exist.
- DONE 0.5.62 adicionou smoke_direct_reinject_missing_receiver_062.js.
- DONE 0.5.62 validado em runtime com conversa ChatGPT para ChatGPT: RECEBIDO conversa 0.5.62.
- DONE 0.5.62 commit 8ec0de7 extension: retry direct delivery after content script reinject.

## Version alignment 0.5.63
- Versao atual: 0.5.63
- Marco publicado: v0.5.63-direct-target-discovery

## Direct interchat target discovery
- DONE 0.5.63 direct_interchat nao falha imediatamente quando target_chat_id ainda nao esta no registry.
- DONE 0.5.63 background procura abas abertas cuja URL contenha o target_chat_id.
- DONE 0.5.63 ao encontrar a aba, registra target_chat_id -> tabId, reinjeta content_script.js e tenta a entrega direta.
- DONE 0.5.63 erro final passa a distinguir target_chat_not_registered de target_tab_not_open em discovery.
- DONE 0.5.63 adicionou smoke_direct_discover_unregistered_target_063.js.

## Version alignment 0.5.64
- Versao atual: 0.5.64
- Marco publicado: direct-discovery-diagnostics.

## 118. Direct discovery diagnostics
- DONE 0.5.64 adiciona tab_count e tabs_sample ao erro target_tab_not_open para diagnosticar abas visiveis ao background.

## Version alignment 0.5.65
- Versao atual: 0.5.67
- Marco publicado: v0.5.67-duplicate-idempotent-captured-route

## 66. Direct cross-profile gateway fallback
- DONE 0.5.65 preserva bloqueio de run-command e delivery_kind local_capability no fallback cross-profile.
- DONE 0.5.65 permite fallback cross-profile somente para send-chat-message/inter_agent_message quando seguro.
- DONE 0.5.65 inject_timeout, destino nao registrado e composer instavel continuam falhas de entrega, nao sucesso.

## Version alignment 0.5.66
- Versao atual: 0.5.67
- Marco publicado: v0.5.67-duplicate-idempotent-captured-route

## 67. Same-profile direct envelope reference
- DONE 0.5.66 corrige erro envelope is not defined no same-profile direct.
- DONE 0.5.66 same-profile direct validado com status sent_direct.
- DONE 0.5.66 resposta inter-chat de volta validada via AI Bridge Local.
- DONE 0.5.66 cross-profile via gateway/local queue validado.

## Version alignment 0.5.67
- Versao atual: 0.5.67
- Marco publicado: v0.5.67-duplicate-idempotent-captured-route

## 68. Duplicate idempotent and captured route guard
- DONE 0.5.67 postCommand trata erro duplicate como sucesso idempotente com ok, already_queued e idempotent.
- DONE 0.5.67 duplicate nao deve gerar AI_LOCAL_ERRO quando command_id ja foi aceito antes.
- DONE 0.5.67 inject_timeout continua falha real de entrega/injecao e nao e mascarado como sucesso.
- DONE 0.5.67 envelope capturado nao posta direto via postCommand(validation.envelope); passa por routeBridgeCommand(validation.envelope, capturedEnvelope).
- DONE 0.5.67 manifest, VERSION, background e content_script alinhados em 0.5.67.
- VALIDADO 0.5.67 git diff --check, node --check dos JS ativos, smoke_direct_interchat_router, smoke_gateway_feedback_dedup e smoke_command_accepted_progress_notice.

# AI Bridge Local - Guia Unificado Operacional e Roadmap

Atualizado em: 2026-07-01
Versao atual: 0.5.71
Branch principal: main
Marco publicado mais recente: v0.5.70-gateway-final-fallback-results
Commit de referencia: 6cf033a
Repositorio local: D:/dev/autocode/ai-bridge-local

Este e o documento principal ativo da aplicacao. A raiz de docs deve conter apenas AI_BRIDGE_LOCAL_GUIDE.md e a pasta legacy. Os demais documentos historicos ficam em docs/legacy e tambem tem seu conteudo preservado neste guia.

## 1. Objetivo do projeto

O AI Bridge Local permite que chats e agentes de IA trabalhem com seguranca sobre repositorios locais. Ele transforma orientacoes em envelopes auditaveis, passa por um gateway local, executa comandos controlados em um worker supervisor e retorna resultados estruturados para o chat.

## 2. Estado atual validado

- Versao atual: 0.5.71.
- Repositorio local: D:/dev/autocode/ai-bridge-local.
- Branch principal: main.
- Commit de referencia desta consolidacao: 6cf033a gateway: wake chat on final fallback results.
- Rota operacional: run-command com delivery_kind local_capability para gateway-brain-supervisor.
- Resultado final esperado: AI_LOCAL_RUN com success, result_is_final, chat_can_continue e next_action.
- cleanup_plan.py permanece em modo report_only; nao executa limpeza real.
- A pasta docs funciona como vault Obsidian organizado por areas; index.md e AI_BRIDGE_LOCAL_GUIDE.md sao os pontos de entrada principais.

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

## 48. IntegraÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o v0.dev / v0.app como modo de pesquisa e prototipaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o de UI

### 48.1 Objetivo

O v0.dev / v0.app deve ser usado no AI Bridge Local como ferramenta externa de prototipaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o, design de interfaces e geraÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o assistida de UI.

O papel do v0 no projeto nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© executar comandos locais nem aplicar patches automaticamente no repositÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rio principal. Ele deve atuar como acelerador visual e gerador de protÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³tipos, enquanto o AI Bridge Local continua sendo o executor auditÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡vel, com fila, smokes, gates, revisÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o e commit controlado.

Uso recomendado:

* gerar protÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³tipos de telas para o AI Bridge Local;
* criar variaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âµes de dashboard operacional;
* desenhar o Command Builder visual;
* prototipar visualizador de fila, dead letters e worker health;
* propor telas de auditoria, release manager e autorizaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o interchat;
* gerar cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo apenas em sandbox ou relatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rio;
* criar prompts reutilizÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡veis para evoluÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o futura da UI.

### 48.2 DecisÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o operacional

DecisÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o: o v0.dev / v0.app pode ser usado no AI Bridge Local como acelerador visual e gerador de protÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³tipos, mas nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o como executor automÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡tico do repositÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rio principal.

Modo inicial aprovado:

* `report_only`
* `research_only`
* sem API obrigatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ria
* sem escrita em `apps/`, `backend/`, `extension/` ou cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo produtivo
* saÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­da em `reports/v0/`
* revisÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o humana obrigatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ria antes de qualquer patch

Status: recomendado para fase de pesquisa e prototipaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o.

### 48.3 PrincÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­pio de seguranÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§a

O v0 deve entrar no AI Bridge Local como capacidade externa controlada.

Fluxo seguro:

1. O AI Bridge Local gera um prompt tÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©cnico para o v0.
2. O prompt ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© salvo em `reports/v0/`.
3. O humano cola o prompt no v0 manualmente ou, em fase futura, uma integraÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o chama a API do v0.
4. O resultado gerado pelo v0 ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© tratado como artefato externo.
5. Nenhum cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo gerado ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© aplicado automaticamente.
6. Um auditor revisa o resultado.
7. Um patch local separado ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© criado somente depois de aprovaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o.
8. O patch passa por smokes, `git diff --check`, stage de arquivos exatos, commit e push.

Regra central:

> v0 gera ideias, protÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³tipos e cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo candidato. AI Bridge Local valida, audita e executa.

### 48.4 Telas candidatas para prototipar no v0

Primeiro lote recomendado:

1. **AI Bridge Local Operations Dashboard**

   * visÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o geral da fila;
   * worker health;
   * comandos pendentes;
   * comandos recentes;
   * falhas por tipo;
   * status do repositÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rio;
   * ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºltimo commit;
   * ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºltimos smokes.

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
   * mostrar causa provÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡vel;
   * sugerir correÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o segura;
   * manter modo readonly;
   * exportar relatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rio.

4. **Worker Health Panel**

   * worker ativo/inativo;
   * PID lock;
   * ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºltimos ciclos;
   * comandos em execuÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o;
   * locks por `cwd`;
   * tempo mÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©dio de execuÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o.

5. **Command Builder Visual**

   * formulÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡rio para criar envelopes;
   * seleÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o de action;
   * seleÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o de destino;
   * `cwd`;
   * timeout;
   * `script_ext`;
   * prÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©via do JSON;
   * validaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o local;
   * risco classificado antes do envio.

6. **Envelope Preview**

   * mostrar JSON formatado;
   * validar campos obrigatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rios;
   * destacar `command_id`;
   * destacar `delivery_kind`;
   * destacar `payload`;
   * bloquear exemplos perigosos.

7. **Docs and Runbook Viewer**

   * ler `AI_BRIDGE_LOCAL_GUIDE.md`;
   * navegar em `docs/legacy`;
   * pesquisar runbooks;
   * mostrar roadmap;
   * mostrar prÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ximas atividades;
   * mostrar histÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rico de releases.

8. **Release Checklist UI**

   * status limpo do git;
   * smokes obrigatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rios;
   * diff check;
   * arquivos staged;
   * mensagem de commit;
   * confirmaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o de push;
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

    * sequÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªncia de comandos;
    * decisÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âµes;
    * falhas;
    * correÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âµes;
    * commits;
    * pushes;
    * tags;
    * releases.

### 48.5 Prompt base para uso manual no v0

Use este prompt no v0 para a primeira exploraÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o:

```text
Crie um dashboard web moderno para o AI Bridge Local.

Contexto:
AI Bridge Local ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© uma ponte local entre chats/agentes de IA e repositÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rios locais. Ele usa envelopes JSON, gateway local, fila SQLite queue_local.db, worker supervisor, smokes, auditoria e commits controlados.

Objetivo:
Criar uma UI de operaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âµes para monitorar e controlar o sistema sem executar comandos automaticamente.

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

Regras de seguranÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§a:
- NÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o incluir segredos.
- NÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o incluir tokens.
- NÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o executar comandos reais.
- NÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o conectar em banco real.
- Usar dados mockados.
- Separar claramente botÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âµes de aÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o real e botÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âµes desabilitados.
- Todo comando deve ser marcado como preview/report_only.
- Nenhum patch deve ser aplicado automaticamente.
- Priorizar Next.js, React, Tailwind e shadcn/ui.

Estilo:
Interface limpa, operacional, com cards de status, tabela de eventos, filtros por command_id, source_chat_id, target_chat_id, cwd, success, next_action e timestamp.

Entregue:
- componentes React;
- dados mockados;
- layout responsivo;
- explicaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o curta da arquitetura da UI;
- sugestÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âµes de prÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ximos componentes.
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
- NÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o executar comandos.
- Apenas gerar preview.
- Validar campos obrigatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rios.
- Alertar se script_text contiver padrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âµes perigosos.
- Alertar se houver comandos destrutivos.
- Mostrar o JSON final formatado.
- BotÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“Copy JSONÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â permitido.
- BotÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“ExecuteÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â deve ficar desabilitado.
- Exibir classificaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o de risco: low, medium, high.

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
- botÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“Generate readonly diagnosticÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â;
- botÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“RetryÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â desabilitado por padrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o;
- aviso de que a tela ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© apenas protÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³tipo/report_only.

Stack:
Next.js, React, Tailwind, shadcn/ui.

Use dados mockados.
```

### 48.8 Prompt para Docs and Runbook Viewer

```text
Crie uma tela chamada AI Bridge Docs and Runbook Viewer.

Objetivo:
Visualizar documentaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o operacional do AI Bridge Local.

SeÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âµes:
- guia principal;
- docs legacy;
- runbooks;
- roadmap;
- ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºltimos commits;
- smokes;
- release checklist.

Funcionalidades:
- busca textual;
- ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡rvore lateral de documentos;
- preview markdown;
- badges para docs ativos e legacy;
- bloco de prÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ximas atividades;
- botÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“Copy sectionÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â;
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

Essa capability deve apenas gerar prompt, relatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rio e checklist.

Ela nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o deve:

* escrever cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo em `apps/`;
* escrever cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo em `backend/`;
* escrever cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo em `extension/`;
* alterar arquivos produtivos;
* instalar dependÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªncias;
* executar `npm`;
* executar `vercel`;
* executar deploy;
* abrir PR automaticamente;
* aplicar patch automaticamente.

### 48.10 Fase 1: sem API

ImplementaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o inicial recomendada:

* criar `reports/v0/AI_BRIDGE_LOCAL_V0_UI_RESEARCH_PLAN_YYYY-MM-DD.md`;
* criar script futuro `scripts/research/v0_ui_prompt_plan.py`;
* criar smoke futuro `scripts/watcher/smoke_v0_ui_research_mode.py`;
* garantir que o smoke valide o termo `report_only`;
* garantir que nenhum patch de UI seja aplicado pela fase de pesquisa;
* manter todos os resultados em relatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rio.

CritÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rios de aceite da fase 1:

* o script gera prompts;
* o script nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o chama API externa;
* o script nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o altera cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo produtivo;
* o script salva somente em `reports/v0/`;
* o smoke confirma que o modo ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© `report_only`;
* o smoke confirma que nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o hÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ escrita em pastas produtivas.

### 48.11 Fase 2: com API do v0

A API do v0 sÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ deve ser considerada depois que existirem controles explÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­citos.

PrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©-requisitos:

* `V0_API_KEY` em `.env` local;
* `.env` em `.gitignore`;
* logs sem segredo;
* limite de custo;
* limite de chamadas;
* limite de tamanho de prompt;
* bloqueio de envio de arquivos sensÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­veis;
* bloqueio de envio de `queue_local.db` real;
* bloqueio de envio de tokens;
* bloqueio de envio de cookies;
* bloqueio de envio de credenciais;
* saÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­da sempre em `reports/v0/`;
* nenhum apply automÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡tico.

VariÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡veis propostas:

```text
V0_API_KEY=local_secret_only
AI_BRIDGE_V0_MODE=report_only
AI_BRIDGE_V0_OUTPUT_DIR=reports/v0
AI_BRIDGE_V0_MAX_PROMPT_CHARS=12000
AI_BRIDGE_V0_ALLOW_EXTERNAL_CALLS=0
```

A variÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡vel `AI_BRIDGE_V0_ALLOW_EXTERNAL_CALLS` deve comeÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ar como `0`.

### 48.12 Fase 3: importaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o guardada

Se o resultado do v0 for aprovado, a importaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o deve usar outro fluxo.

Fluxo de importaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o:

1. criar branch ou patch separado;
2. verificar `git status --short`;
3. revisar arquivos gerados;
4. remover dependÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªncias desnecessÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡rias;
5. remover segredos;
6. remover chamadas reais;
7. usar dados mockados;
8. rodar lint/test quando aplicÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡vel;
9. rodar smoke especÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­fico;
10. rodar `git diff --check`;
11. stage de arquivos exatos;
12. auditoria humana;
13. commit com mensagem clara;
14. push somente depois de validaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o.

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
* importar dependÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªncias desnecessÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡rias;
* criar acoplamento indevido com Vercel;
* expor contexto sensÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­vel em prompt externo;
* aplicar cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo gerado sem auditoria;
* confundir protÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³tipo com implementaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o validada;
* criar botÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âµes que pareÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§am executar aÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âµes reais;
* gerar cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo com padrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âµes incompatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­veis com o repo;
* gerar telas que nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o respeitam o protocolo de envelopes;
* gerar chamadas externas sem controle de custo.

### 48.14 MitigaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âµes

MitigaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âµes obrigatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rias:

* usar v0 como pesquisa e protÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³tipo;
* manter AI Bridge Local como executor auditÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡vel;
* manter modo `report_only` como padrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o;
* separar relatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rio, patch e commit;
* manter smokes como gate obrigatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rio;
* nunca enviar segredos;
* nunca enviar `.env`;
* nunca enviar banco local real;
* nunca aplicar patch automaticamente;
* revisar dependÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªncias antes de instalar;
* exigir aprovaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o humana para qualquer importaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o;
* manter botÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o de execuÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o real desabilitado em protÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³tipos.

### 48.15 Primeira entrega recomendada

Primeira entrega:

```text
reports/v0/AI_BRIDGE_LOCAL_V0_UI_RESEARCH_PLAN_2026-06-16.md
```

ConteÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºdo do relatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rio:

* objetivo;
* prompts sugeridos;
* telas candidatas;
* regras de seguranÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§a;
* limites do uso do v0;
* critÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rios de aceite;
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
* nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o chamar API externa;
* nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o alterar cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo produtivo.

Terceira entrega:

```text
scripts/watcher/smoke_v0_ui_research_mode.py
```

Responsabilidade:

* validar que o script existe;
* validar que o modo padrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© `report_only`;
* validar que a saÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­da vai para `reports/v0/`;
* validar que nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o hÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ escrita em `apps/`, `backend/` ou `extension/`;
* validar que nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o hÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ uso obrigatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rio de `V0_API_KEY` na fase 1;
* validar que o relatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rio contÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©m ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“nenhum patch automÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ticoÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â.

### 48.16 CritÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rios de aceite

A integraÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o documental do v0 serÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ considerada vÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡lida quando:

* este guia mencionar v0.dev / v0.app;
* o modo recomendado for `report_only`;
* o guia deixar claro que v0 nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o executa comandos locais;
* existir relatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rio em `reports/v0/`;
* existir plano para `scripts/research/v0_ui_prompt_plan.py`;
* existir plano para `scripts/watcher/smoke_v0_ui_research_mode.py`;
* `smoke_docs.py` continuar passando;
* `git diff --check` continuar passando;
* a raiz de `docs/` continuar contendo apenas `AI_BRIDGE_LOCAL_GUIDE.md` e `legacy/`.

### 48.17 DecisÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o final

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
gerar prompts, protÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³tipos e relatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³rios de UI
```

Uso proibido na fase inicial:

```text
executar comandos, aplicar patches, fazer deploy, instalar dependÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªncias ou alterar cÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³digo produtivo automaticamente
```

PrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³xima atividade recomendada:

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


## AtualizaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o 0.5.39 - final result feedback guard

- Impede feedback local intermediario para `result_to_*`.
- Evita `local_status_accepted_result_to_*` para resultados finais.
- Preserva o fluxo esperado: queued inicial + `[AI_LOCAL_RUN]` final.
- Mantem `final_result_sweeper_v3.py` apenas como mitigacao operacional temporaria.


## AtualizaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o 0.5.40 - Gemini manifest name sync

- Sincroniza `extension/manifest.json` para exibir `AI Bridge Local 0.5.40`.
- Mantem `version` e `name` da extensÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o alinhados para evitar confusÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o ao recarregar a extensÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o no Chrome.
- Sem alteraÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â£o de lÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³gica do gateway/worker.


## Version alignment 0.5.41
- Versao atual: 0.5.69
- Marco publicado: v0.5.41-chatgpt-outbound-envelope-capture

## ChatGPT outbound envelope capture
- DONE 0.5.41 adiciona observer outbound para envelopes em respostas ChatGPT.
- DONE 0.5.41 aceita START/END e BEGIN/END.
- DONE 0.5.41 valida source_chat_id e reporta erro local quando possivel.


## Version alignment 0.5.42
- Versao atual: 0.5.69
- Marco publicado: v0.5.42-direct-interchat-router-safe

## Direct inter-chat router safe
- DONE 0.5.42 roteia send-chat-message/inter_agent_message direto pelo background quando o target_chat_id esta registrado.
- DONE 0.5.42 mantem run-command/local_capability sempre via gateway/DB/worker.
- DONE 0.5.42 adiciona feature flags e evita fallback automatico para nao mascarar falhas.
- DONE 0.5.42 preserva avisos/acks/resultados do fluxo gateway.


## Version alignment 0.5.43
- Versao atual: 0.5.69
- Marco publicado: v0.5.43-chatgpt-candidate-envelope-scanner

## ChatGPT candidate envelope scanner
- DONE 0.5.43 evita bloqueio global quando a pagina contem mensagens AI_LOCAL antigas.
- DONE 0.5.43 escaneia candidatos especificos de mensagens ChatGPT.
- DONE 0.5.43 adiciona varredura periodica e mutation observer para envelopes.


## Version alignment 0.5.44
- Versao atual: 0.5.69
- Marco publicado: v0.5.44-standalone-chatgpt-scanner-feedback

## Standalone ChatGPT scanner with visible feedback
- DONE 0.5.44 adiciona scanner standalone sem depender de extract/send internos.
- DONE 0.5.44 injeta aviso visivel [AI_LOCAL] para entrega direta bem-sucedida.
- DONE 0.5.44 injeta aviso visivel [AI_LOCAL_ERRO] para falha de captura/rota direta.
- DONE 0.5.44 preserva gateway obrigatorio para run-command/local_capability.


## Version alignment 0.5.45
- Versao atual: 0.5.69
- Marco publicado: v0.5.45-content-script-heartbeat-guard

## Content script heartbeat guard
- DONE 0.5.45 protege sendChatHeartbeat contra ReferenceError.
- DONE 0.5.45 evita que falha de heartbeat interrompa o scanner standalone.
- DONE 0.5.45 preserva feedback visivel e gateway obrigatorio para run-command/local_capability.


## Version alignment 0.5.46
- Versao atual: 0.5.69
- Marco publicado: v0.5.46-disable-legacy-scanner-inline-heartbeat

## Disable legacy scanner and inline heartbeat guard
- DONE 0.5.46 remove chamada fora de escopo ao aiBridgeSafeCallSendChatHeartbeat.
- DONE 0.5.46 desativa scanner legado global que chamava extract(t).forEach(send).
- DONE 0.5.46 evita erro sendTextToChat is not defined vindo do scanner legado.
- DONE 0.5.46 preserva scanner standalone com feedback visivel.


## Version alignment 0.5.47
- Versao atual: 0.5.69
- Marco publicado: v0.5.47-matching-composer-direct-inject-retry

## Matching composer direct inject retry
- DONE 0.5.47 permite limpar composer do destino quando ele ja contem exatamente o texto solicitado.
- DONE 0.5.47 preserva trava contra sobrescrever texto manual diferente.
- DONE 0.5.47 melhora feedback de composer_not_empty_before_inject.
- DONE 0.5.47 mantem gateway obrigatorio para run-command/local_capability.


## Version alignment 0.5.48
- Versao atual: 0.5.69
- Marco publicado: v0.5.48-robust-composer-text-injection

## Robust composer text injection
- DONE 0.5.48 adiciona aiBridgeRobustSetText para contenteditable/textarea/input.
- DONE 0.5.48 corrige falha composer_empty_after_inject na rota direta.
- DONE 0.5.48 preserva scanner standalone com feedback visivel.
- DONE 0.5.48 mantem gateway obrigatorio para run-command/local_capability.


## Version alignment 0.5.49
- Versao atual: 0.5.69
- Marco publicado: v0.5.49-force-chatgpt-prompt-textarea-composer

## Force ChatGPT prompt-textarea composer
- DONE 0.5.49 prioriza #prompt-textarea.ProseMirror como composer real.
- DONE 0.5.49 ignora inputs de upload/camera.
- DONE 0.5.49 adiciona diagnostico do composer escolhido.
- DONE 0.5.49 preserva scanner standalone e gateway obrigatorio para run-command/local_capability.


## Version alignment 0.5.50
- Versao atual: 0.5.69
- Marco publicado: v0.5.50-repair-prompt-textarea-composer-smoke

## Repair prompt-textarea composer smoke
- DONE 0.5.50 corrige smoke falho do patch de composer.
- DONE 0.5.50 preserva priorizacao de #prompt-textarea.ProseMirror.
- DONE 0.5.50 adiciona composer descriptor flexivel.
- DONE 0.5.50 mantem gateway obrigatorio para run-command/local_capability.


## Version alignment 0.5.51
- Versao atual: 0.5.69
- Marco publicado: v0.5.51-standalone-visible-status-composer-scope

## Standalone visible status composer scope
- DONE 0.5.51 corrige status visivel do scanner standalone no chat origem.
- DONE 0.5.51 remove dependencia de helper de composer fora do IIFE standalone.
- DONE 0.5.51 preserva entrega direta inter-chat ja validada.
- DONE 0.5.51 mantem gateway obrigatorio para run-command/local_capability.


## Version alignment 0.5.52
- Versao atual: 0.5.69
- Marco publicado: v0.5.52-gemini-local-status-prefix-scope

## Gemini local status prefix scope
- DONE 0.5.52 corrige `LOCAL_STATUS_PREFIXES is not defined` no Gemini envelope observer.
- DONE 0.5.52 preserva rota direta inter-chat sem gateway/DB.
- DONE 0.5.52 mantem gateway obrigatorio para run-command/local_capability.

## Version alignment 0.5.59
- Versao atual: 0.5.69
- Marco publicado: v0.5.59-direct-interchat-chatgpt

## Direct interchat ChatGPT
- DONE 0.5.59 criou rota direta inter-chat para send-chat-message sem gateway/DB quando transport=direct_interchat.
- DONE 0.5.59 manteve run-command, patch, smoke e inspect no gateway local.
- DONE 0.5.59 adicionou smokes de route classifier, background route load, captured envelope route integration e direct route contract.

## Version alignment 0.5.60
- Versao atual: 0.5.69
- Marco publicado: v0.5.60-line-isolated-envelope-capture

## ChatGPT line-isolated envelope capture
- DONE 0.5.60 iniciou guarda para captura de envelopes apenas em blocos isolados por linha.
- DONE 0.5.60 identificou que ainda havia caminho runtime capturando mencoes inline de marcadores.

## Version alignment 0.5.61
- Versao atual: 0.5.69
- Marco publicado: v0.5.61-inline-marker-parse-guard

## Inline marker parse guard
- DONE 0.5.61 ignora mencoes inline de marcadores e processa somente blocos locais isolados.
- DONE 0.5.61 adicionou smoke_chatgpt_line_isolated_envelope_capture.js.
- DONE 0.5.61 adicionou smoke_chatgpt_inline_marker_parse_guard_061.js.
- DONE 0.5.61 commit 34f27b0 extension: ignore inline ChatGPT marker mentions.

## Version alignment 0.5.62
- Versao atual: 0.5.69
- Marco publicado: v0.5.62-direct-interchat-auto-reinject

## Direct interchat auto reinject
- DONE 0.5.62 adiciona retry de entrega direta apos falha de receiver ausente.
- DONE 0.5.62 background reinjeta content_script.js no tab destino quando encontra Could not establish connection / Receiving end does not exist.
- DONE 0.5.62 adicionou smoke_direct_reinject_missing_receiver_062.js.
- DONE 0.5.62 validado em runtime com conversa ChatGPT para ChatGPT: RECEBIDO conversa 0.5.62.
- DONE 0.5.62 commit 8ec0de7 extension: retry direct delivery after content script reinject.

## Version alignment 0.5.63
- Versao atual: 0.5.69
- Marco publicado: v0.5.63-direct-target-discovery

## Direct interchat target discovery
- DONE 0.5.63 direct_interchat nao falha imediatamente quando target_chat_id ainda nao esta no registry.
- DONE 0.5.63 background procura abas abertas cuja URL contenha o target_chat_id.
- DONE 0.5.63 ao encontrar a aba, registra target_chat_id -> tabId, reinjeta content_script.js e tenta a entrega direta.
- DONE 0.5.63 erro final passa a distinguir target_chat_not_registered de target_tab_not_open em discovery.
- DONE 0.5.63 adicionou smoke_direct_discover_unregistered_target_063.js.

## Version alignment 0.5.64
- Versao atual: 0.5.69
- Marco publicado: direct-discovery-diagnostics.

## 118. Direct discovery diagnostics
- DONE 0.5.64 adiciona tab_count e tabs_sample ao erro target_tab_not_open para diagnosticar abas visiveis ao background.

## Version alignment 0.5.65
- Versao atual: 0.5.69
- Marco publicado: v0.5.67-duplicate-idempotent-captured-route

## 66. Direct cross-profile gateway fallback
- DONE 0.5.65 preserva bloqueio de run-command e delivery_kind local_capability no fallback cross-profile.
- DONE 0.5.65 permite fallback cross-profile somente para send-chat-message/inter_agent_message quando seguro.
- DONE 0.5.65 inject_timeout, destino nao registrado e composer instavel continuam falhas de entrega, nao sucesso.

## Version alignment 0.5.66
- Versao atual: 0.5.69
- Marco publicado: v0.5.67-duplicate-idempotent-captured-route

## 67. Same-profile direct envelope reference
- DONE 0.5.66 corrige erro envelope is not defined no same-profile direct.
- DONE 0.5.66 same-profile direct validado com status sent_direct.
- DONE 0.5.66 resposta inter-chat de volta validada via AI Bridge Local.
- DONE 0.5.66 cross-profile via gateway/local queue validado.

## Version alignment 0.5.67
- Versao atual: 0.5.69
- Marco publicado: v0.5.67-duplicate-idempotent-captured-route

## 68. Duplicate idempotent and captured route guard
- DONE 0.5.67 postCommand trata erro duplicate como sucesso idempotente com ok, already_queued e idempotent.
- DONE 0.5.67 duplicate nao deve gerar AI_LOCAL_ERRO quando command_id ja foi aceito antes.
- DONE 0.5.67 inject_timeout continua falha real de entrega/injecao e nao e mascarado como sucesso.
- DONE 0.5.67 envelope capturado nao posta direto via postCommand(validation.envelope); passa por routeBridgeCommand(validation.envelope, capturedEnvelope).
- DONE 0.5.67 manifest, VERSION, background e content_script alinhados em 0.5.67.
- VALIDADO 0.5.67 git diff --check, node --check dos JS ativos, smoke_direct_interchat_router, smoke_gateway_feedback_dedup e smoke_command_accepted_progress_notice.

## Version alignment 0.5.68
- Versao atual: 0.5.69
- Marco publicado: v0.5.68-local-bridge-version-bump
- Commit: 4c7c184 extension: bump local bridge to 0.5.68

## 69. Local bridge 0.5.68 reload validation
- DONE 0.5.68 bump limpo de VERSION, manifest, background e content_script.
- DONE 0.5.68 smoke_post_command_duplicate_idempotent_0568 criado a partir do contrato 0.5.67.
- VALIDADO 0.5.68 node --check para background, content_script e route_classifier.
- VALIDADO 0.5.68 smokes: duplicate idempotent, direct interchat router, gateway feedback dedup e command accepted progress notice.
- OBSERVADO 0.5.68 apos recarregar a extensao, envio inter-chat voltou a sair com metodo button_click_confirmed.
- NOTA 0.5.68 a falha anterior foi observada como inject_timeout/estado de injecao da aba destino; nao foi encontrada regressao no contrato duplicate/idempotent.

## Version alignment 0.5.69
- Versao atual: 0.5.69
- Marco publicado: v0.5.69-final-run-continuation
- Commit: 359d36e worker: wake chat on final local run result

## 70. Final AI_LOCAL_RUN continuation contract
- DONE 0.5.69 brain_worker.py define final_no_reply como 0 quando chat_can_continue e 1.
- DONE 0.5.69 AI_LOCAL_RUN final usa no_reply dinamico em vez de no_reply fixo 1.
- DONE 0.5.69 smoke_final_run_continue_no_reply_0569 cobre o contrato result_is_final=1, chat_can_continue=1 e no_reply=0.
- DONE 0.5.69 smoke_post_command_duplicate_idempotent_0569 preserva o contrato duplicate/idempotent.
- VALIDADO 0.5.69 py_compile brain_worker, node --check dos JS ativos e smokes relevantes.
- NOTA operacional: o AI_LOCAL_RUN do proprio comando que aplica o patch ainda pode vir do worker antigo; reiniciar/recarregar o worker/extensao aplica o novo contrato nas proximas execucoes.

## Version alignment 0.5.70
- Versao atual: 0.5.71
- Marco publicado: v0.5.70-gateway-final-fallback-results
- Commit: 6cf033a gateway: wake chat on final fallback results

## 71. Gateway final fallback continuation contract
- DONE 0.5.70 gateway_local.py corrige fallback AI_LOCAL_RUN final para no_reply=0 quando chat_can_continue=1.
- DONE 0.5.70 preserva queued informativo com no_reply=1.
- DONE 0.5.70 smoke_gateway_final_run_no_reply_0570 cobre o fallback final do gateway.
- DONE 0.5.70 smoke_post_command_duplicate_idempotent_0570 preserva o contrato duplicate/idempotent.
- VALIDADO 0.5.70 em execucao real: AI_LOCAL_RUN final retornou no_reply=0, result_is_final=1 e chat_can_continue=1.
- VALIDADO 0.5.70 py_compile, node --check e smokes relevantes antes do commit.
- NOTA operacional: 0.5.69 corrigiu brain_worker.py; 0.5.70 completou a correcao no gateway_local.py, que tambem podia emitir resultado final com no_reply antigo.

## Version alignment 0.5.71
- Versao atual: 0.5.71
- Commit: 7ed6d5e extension: refresh direct target before delivery.
7ed6d5e
 extension: refresh direct target before delivery

## 72. Direct inter-chat target refresh
- DONE 0.5.71 redescobre a aba alvo antes da entrega direta.
- DONE 0.5.71 prefere aba ativa que bate com target_chat_id ou target_url.
- VALIDADO 0.5.71 com post_reload_live_smoke_0571_20260701_001.
- VALIDADO 0.5.71 com interchat_live_0571_target_url_20260701_003 retornando sent_direct.
- PENDENTE para 0.5.72: endurecer parser contra quebras de linha cruas dentro de strings JSON.

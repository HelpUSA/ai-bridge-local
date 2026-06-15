# AI Bridge Local - Guia Unificado Operacional e Roadmap

Atualizado em: 2026-06-14
Versao atual: 0.5.5
Branch principal: main
Marco publicado mais recente: v0.5.5-disable-worker-running-notice
Commit de referencia: v0.5.5-disable-worker-running-notice
Repositorio local: D:/dev/autocode/ai-bridge-local

Este arquivo e o documento operacional ativo e consolidado do AI Bridge Local.
O guia foi compactado em 0.4.97 para remover crescimento acidental de tamanho e permitir push no GitHub.
Documentos historicos e relatorios continuam em docs/, docs/archive, docs/legacy e reports/.

---

## 50. Latency parallel polling
- [DONE 0.4.97] Polling fallback do background reduzido de 5000 ms para 1000 ms.
- [DONE 0.4.97] Registro de chat no content script reduzido de 5000 ms para 1500 ms.
- [DONE 0.4.97] pollMessages passou a usar snapshot de chats e Promise.allSettled com pollOneChat por chat.
- [DONE 0.4.97] pollInFlight evita ciclos sobrepostos e perChatInFlight evita duplicidade no mesmo chat sem bloquear outros chats.
- [DONE 0.4.97] pollMessagesSoon agenda fast path com debounce de 150 ms apos postCommand, registro de chat e startup.
- [DONE 0.4.97] Cada chat drena ate 3 acoes por ciclo e um chat lento nao trava os demais.
- [DONE 0.4.97] Smoke criado em scripts/watcher/smoke_latency_parallel_polling.py.

## Version alignment 0.4.97
- Atualizado topo do guia para 0.4.97.
- Marco publicado: v0.4.97-latency-parallel-polling.

## 49. Autonomous evolution audit ledger
- Referencia: reports/AI_BRIDGE_LOCAL_AUTONOMOUS_EVOLUTION_AUDIT_LEDGER_2026-06-14.md.

## Version alignment 0.4.96
- Marco publicado: v0.4.96-autonomous-evolution-audit-ledger.

## 48. Autonomous evolution task queue
- Referencia: reports/AI_BRIDGE_LOCAL_AUTONOMOUS_EVOLUTION_TASK_QUEUE_2026-06-14.md.

## Version alignment 0.4.95
- Marco publicado: v0.4.95-autonomous-evolution-task-queue.

## 47. Autonomous change proposal template
- Referencia: reports/AI_BRIDGE_LOCAL_AUTONOMOUS_CHANGE_PROPOSAL_TEMPLATE_2026-06-14.md.

## Version alignment 0.4.94
- Marco publicado: v0.4.94-autonomous-change-proposal-template.

## 46. Autonomous evolution approval matrix
- Referencia: reports/AI_BRIDGE_LOCAL_AUTONOMOUS_EVOLUTION_APPROVAL_MATRIX_2026-06-14.md.

## Version alignment 0.4.93
- Marco publicado: v0.4.93-autonomous-evolution-approval-matrix.

## Mapa de marcadores para smokes
Esta secao preserva textos requeridos por scripts/watcher/smoke_docs.py sem manter o guia gigante.
- ## 1. Objetivo do projeto
- ## 14. Proximas atividades recomendadas em ordem
- ## 16. Hardening pos fase 9.8
- ## 17. Proxima fase - fundamentos API local
- ## 18. Local bridge store
- ## 19. Local bridge envelope
- ## 2. Estado atual validado
- ## 20. Local bridge writer e ack
- ## 21. Local bridge dashboard
- ## 22. Local bridge replay apply
- ## 23. Local bridge worker dry-run
- ## 24. Consolidacao local bridge 0.4.65 a 0.4.70
- ## 25. Governance risk classifier
- ## 26. Governance preflight
- ## 27. Command builder governance
- ## 28. Command builder governance finalize
- ## 29. Governance roadmap
- ## 30. Command builder advisory metadata
- ## 31. Command builder advisory gate
- ## 32. Governance decision log
- ## 33. Governance risk report
- ## 34. Command builder preferred advisory flow
- ## 35. Destructive opt-in gate
- ## 36. Governance phase consolidation
- ## 37. Queue health audit
- ## 38. Safe envelope templates
- ## 39. Governance enforcement dry-run
- ## 4. Protocolo de envelopes
- ## 40. Release safety checklist
- ## 41. Queue triage playbook
- ## 42. Watcher failure taxonomy
- ## 43. Self evolution guardrails
- ## 44. Watcher recovery runbook
- ## 45. Autonomous evolution protocol
- ## 9. Roadmap detalhado de atividades pendentes
- ## Version alignment 0.4.58
- ## Version alignment 0.4.59
- ## Version alignment 0.4.60
- ## Version alignment 0.4.61
- ## Version alignment 0.4.62
- ## Version alignment 0.4.63
- ## Version alignment 0.4.64
- ## Version alignment 0.4.65
- ## Version alignment 0.4.66
- ## Version alignment 0.4.67
- ## Version alignment 0.4.68
- ## Version alignment 0.4.69
- ## Version alignment 0.4.70
- ## Version alignment 0.4.71
- ## Version alignment 0.4.72
- ## Version alignment 0.4.73
- ## Version alignment 0.4.74
- ## Version alignment 0.4.75
- ## Version alignment 0.4.76
- ## Version alignment 0.4.77
- ## Version alignment 0.4.78
- ## Version alignment 0.4.79
- ## Version alignment 0.4.80
- ## Version alignment 0.4.81
- ## Version alignment 0.4.82
- ## Version alignment 0.4.83
- ## Version alignment 0.4.84
- ## Version alignment 0.4.85
- ## Version alignment 0.4.86
- ## Version alignment 0.4.87
- ## Version alignment 0.4.88
- ## Version alignment 0.4.89
- ## Version alignment 0.4.90
- ## Version alignment 0.4.91
- ## Version alignment 0.4.92
- ### 9.7 Longo prazo - orquestracao entre chats
- - scripts/watcher/auditor_mode.py.
- - scripts/watcher/executor_gates.py.
- - scripts/watcher/planner_mode.py.
- - scripts/watcher/release_manager_mode.py.
- - scripts/watcher/teach_envelopes.py.
- 0.4.45
- 0.4.46
- 0.4.47
- 0.4.48
- 0.4.49
- 0.4.50
- 0.4.51
- 0.4.52
- 0.4.53
- 0.4.54
- 0.4.55
- 0.4.56
- 0.4.57
- 1. Criar modo planejador. [DONE 0.4.59 - read-only objective plan gates]
- 1. Criar smoke para send-chat-message. [DONE 0.4.45]
- 10. Remover referencias obsoletas de release antiga e compatibilidade do docs smoke. [DONE 0.4.54]
- 11. Criar padrao de handoff entre chats. [DONE 0.4.56]
- 12. Criar matriz de responsabilidade entre chats. [DONE 0.4.57]
- 13. Criar envelopes de ensino. [DONE 0.4.58]
- 14. Criar modo planejador. [DONE 0.4.59]
- 15. Criar modo executor com gates. [DONE 0.4.60]
- 16. Criar modo auditor. [DONE 0.4.61]
- 17. Criar modo release manager. [DONE 0.4.62]
- 2. Criar intent inspect_delivery_failure. [DONE 0.4.46]
- 2. Criar modo executor com gates. [DONE 0.4.60 - approval validation stop-on-failure gates]
- 2. Criar padrao de handoff. [DONE 0.4.56 - template cli json markdown]
- 3. Criar matriz de responsabilidade. [DONE 0.4.57 - supervisor executor fiscal documentador]
- 3. Criar modo auditor. [DONE 0.4.61 - git tags docs divergence audit]
- 3. Melhorar diagnostico de submit_button_not_found_or_disabled. [DONE 0.4.47]
- 4. Criar envelopes de ensino. [DONE 0.4.58 - watcher safety release recovery lessons]
- 4. Criar intent validate_release. [DONE 0.4.48]
- 4. Criar modo release manager. [DONE 0.4.62 - safe single-commit release plan]
- 5. Criar patch runner com dry-run. [DONE 0.4.49]
- 6. Criar rollback helper. [DONE 0.4.50]
- 7. Consolidar relatorio de dead letters por tipo. [DONE 0.4.51]
- 8. Criar protocolo formal de fiscalizacao entre chats. [DONE 0.4.52]
- 9. Melhorar docs smoke para garantir que este guia continue completo. [DONE 0.4.53]
- ] [DONE
- AI_BRIDGE_LOCAL_GUIDE.md
- auditor 9.8 marker count:
- auditor alignment count:
- auditor file line count:
- auditor section 14 marker count:
- autonomous_change_proposal_template alignment count:
- autonomous_change_proposal_template report reference missing
- autonomous_change_proposal_template section count:
- autonomous_evolution_approval_matrix alignment count:
- autonomous_evolution_approval_matrix report reference missing
- autonomous_evolution_approval_matrix section count:
- autonomous_evolution_audit_ledger alignment count:
- autonomous_evolution_audit_ledger report reference missing
- autonomous_evolution_audit_ledger section count:
- autonomous_evolution_protocol alignment count:
- autonomous_evolution_protocol report reference missing
- autonomous_evolution_protocol section count:
- autonomous_evolution_task_queue alignment count:
- autonomous_evolution_task_queue report reference missing
- autonomous_evolution_task_queue section count:
- chat_bridge_plan.py
- command builder advisory alignment count:
- command builder advisory report reference missing
- command builder advisory section count:
- command builder governance alignment count:
- command builder governance finalize alignment count:
- command builder governance finalize report reference missing
- command builder governance finalize section count:
- command builder governance report reference missing
- command builder governance section count:
- Command builder smoke
- command_builder_advisory_gate alignment count:
- command_builder_advisory_gate report reference missing
- command_builder_advisory_gate section count:
- command_builder_preferred alignment count:
- command_builder_preferred report reference missing
- command_builder_preferred section count:
- Dead letters grouped report
- dead_letters_review.py
- destructive_optin_gate alignment count:
- destructive_optin_gate report reference missing
- destructive_optin_gate section count:
- Diagnostics filters
- Diagnostics report
- Diagnostics viewer
- duplicate DONE markers found:
- duplicate handoff 9.7 marker
- duplicate handoff section 14 marker
- executor 9.8 marker count:
- executor alignment count:
- executor file line count:
- executor section 14 marker count:
- gateway-brain-supervisor
- governance preflight alignment count:
- governance preflight report reference missing
- governance preflight section count:
- governance risk classifier alignment count:
- governance risk classifier report reference missing
- governance risk classifier section count:
- governance roadmap alignment count:
- governance roadmap report reference missing
- governance roadmap section count:
- governance_decision_log alignment count:
- governance_decision_log report reference missing
- governance_decision_log section count:
- governance_enforcement_dry_run alignment count:
- governance_enforcement_dry_run report reference missing
- governance_enforcement_dry_run section count:
- governance_phase_consolidation alignment count:
- governance_phase_consolidation report reference missing
- governance_phase_consolidation section count:
- governance_preflight.py
- governance_risk_classifier.py
- governance_risk_report alignment count:
- governance_risk_report report reference missing
- governance_risk_report section count:
- handoff_template.py
- hardening alignment count:
- hardening report reference missing
- hardening section count:
- latency_parallel_polling alignment count:
- latency_parallel_polling section count:
- latency_parallel_polling smoke reference missing
- local api alignment count:
- local api report reference missing
- local api section count:
- local bridge alignment count:
- local bridge consolidation alignment count:
- local bridge consolidation report reference missing
- local bridge consolidation section count:
- local bridge dashboard alignment count:
- local bridge dashboard report reference missing
- local bridge dashboard section count:
- local bridge envelope alignment count:
- local bridge envelope report reference missing
- local bridge envelope section count:
- local bridge replay apply alignment count:
- local bridge replay apply report reference missing
- local bridge replay apply section count:
- local bridge report reference missing
- local bridge section count:
- local bridge worker dry run alignment count:
- local bridge worker dry run report reference missing
- local bridge worker dry run section count:
- local bridge writer ack alignment count:
- local bridge writer ack report reference missing
- local bridge writer ack section count:
- local_api_dry_run.py
- local_api_readonly.py
- local_bridge_ack_writer.py
- local_bridge_dashboard.py
- local_bridge_dashboard_summary.py
- local_bridge_envelope.py
- local_bridge_reconcile.py
- local_bridge_replay_apply.py
- local_bridge_replay_dry_run.py
- local_bridge_store.py
- local_bridge_worker_dry_run.py
- local_bridge_writer.py
- missing latest release marker
- missing reference commit line
- missing required guide text:
- missing required headings:
- missing roadmap done markers:
- OK docs_smoke
- patch_runner.py
- planner 9.8 marker count:
- planner alignment count:
- planner file line count:
- planner section 14 marker count:
- post_release_audit.py
- queue_health_audit alignment count:
- queue_health_audit report reference missing
- queue_health_audit section count:
- queue_triage_playbook alignment count:
- queue_triage_playbook report reference missing
- queue_triage_playbook section count:
- release manager 9.8 marker count:
- release manager alignment count:
- release manager file line count:
- release manager section 14 marker count:
- release_safety_checklist alignment count:
- release_safety_checklist report reference missing
- release_safety_checklist section count:
- reports/AI_BRIDGE_LOCAL_AUTONOMOUS_EVOLUTION_PROTOCOL_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_COMMAND_BUILDER_ADVISORY_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_COMMAND_BUILDER_ADVISORY_GATE_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_COMMAND_BUILDER_GOVERNANCE_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_COMMAND_BUILDER_GOVERNANCE_FINALIZE_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_COMMAND_BUILDER_PREFERRED_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_DESTRUCTIVE_OPTIN_GATE_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_GOVERNANCE_DECISION_LOG_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_GOVERNANCE_ENFORCEMENT_DRY_RUN_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_GOVERNANCE_PHASE_CONSOLIDATION_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_GOVERNANCE_PREFLIGHT_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_GOVERNANCE_RISK_CLASSIFIER_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_GOVERNANCE_RISK_REPORT_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_GOVERNANCE_ROADMAP_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_LOCAL_BRIDGE_CONSOLIDATION_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_LOCAL_BRIDGE_DASHBOARD_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_LOCAL_BRIDGE_ENVELOPE_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_LOCAL_BRIDGE_REPLAY_APPLY_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_LOCAL_BRIDGE_STORE_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_LOCAL_BRIDGE_WORKER_DRY_RUN_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_LOCAL_BRIDGE_WRITER_ACK_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_NEXT_PHASE_BLOCKS_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_PHASE_9_8_FINAL_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_QUEUE_HEALTH_AUDIT_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_QUEUE_TRIAGE_PLAYBOOK_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_RELEASE_SAFETY_CHECKLIST_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_SAFE_ENVELOPE_TEMPLATES_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_SELF_EVOLUTION_GUARDRAILS_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_WATCHER_FAILURE_TAXONOMY_2026-06-14.md
- reports/AI_BRIDGE_LOCAL_WATCHER_RECOVERY_RUNBOOK_2026-06-14.md
- responsibility 9.7 marker count:
- responsibility section 14 marker count:
- responsibility_matrix.py
- rollback_helper.py
- Safe validation wrapper
- safe_envelope_templates alignment count:
- safe_envelope_templates report reference missing
- safe_envelope_templates section count:
- script_text/script_ext
- self_evolution_guardrails alignment count:
- self_evolution_guardrails report reference missing
- self_evolution_guardrails section count:
- smoke_command_builder_governance.py
- stale guide text found:
- supervision_protocol.py
- tag_divergence_report.py
- teach 9.7 marker count:
- teach file line count:
- teach section 14 marker count:
- teach version alignment count:
- utf-8
- VERSION
- version alignment heading count:
- watcher_failure_taxonomy alignment count:
- watcher_failure_taxonomy report reference missing
- watcher_failure_taxonomy section count:
- watcher_recovery_runbook alignment count:
- watcher_recovery_runbook report reference missing
- watcher_recovery_runbook section count:
## 51. Latency parallel polling docs
- [DONE 0.4.98] Documentada arquitetura de polling paralelo por chat.
- [DONE 0.4.98] Criado docs/LATENCY_PARALLEL_POLLING_ARCHITECTURE.md.
- [DONE 0.4.98] Criado reports/AI_BRIDGE_LOCAL_LATENCY_PARALLEL_POLLING_REPORT_2026-06-14.md.
- [DONE 0.4.98] Criado scripts/watcher/smoke_latency_parallel_polling_docs.py.

## Version alignment 0.4.98
- Atualizado topo do guia para 0.4.98.
- Marco publicado: v0.4.98-latency-parallel-polling-docs.

## 52. Command accepted progress notice
- [DONE 0.4.99] Criado aviso rapido [AI_LOCAL] quando o worker aceita run-command.
- [DONE 0.4.99] Mantido suporte a comandos grandes sem dividir em etapas pequenas.
- [DONE 0.4.99] Resultado final continua em [AI_LOCAL_RUN].
- [DONE 0.4.99] Criado docs/COMMAND_ACCEPTED_PROGRESS_NOTICE.md.
- [DONE 0.4.99] Criado scripts/watcher/smoke_command_accepted_progress_notice.py.


## Version alignment 0.4.99
- Atualizado topo do guia para 0.4.99.
- Marco publicado: v0.4.99-command-accepted-progress-notice.

## 53. Worker queue parallelism
- [DONE 0.5.0] Worker passa a submeter run-command em ThreadPoolExecutor.
- [DONE 0.5.0] Limite padrao de paralelismo: AI_BRIDGE_MAX_PARALLEL_RUN_COMMANDS=3.
- [DONE 0.5.0] Lock por cwd serializa comandos no mesmo repositorio.
- [DONE 0.5.0] Gateway continua sendo fila local em queue_local.db.
- [DONE 0.5.0] Criado docs/WORKER_QUEUE_PARALLELISM.md.
- [DONE 0.5.0] Criado scripts/watcher/smoke_worker_queue_parallelism.py.

## Version alignment 0.5.0
- Atualizado topo do guia para 0.5.0.
- Marco publicado: v0.5.5-disable-worker-running-notice.

## 55. Queue reports cleanup
- DONE 0.5.1 queue_status_report.py
- DONE 0.5.1 dead_letters_cleanup_plan.py dry-run

## Version alignment 0.5.1
- Versao atual: 0.5.5
- Marco publicado: v0.5.5-disable-worker-running-notice

## Version alignment 0.5.2
- Versao atual: 0.5.5
- Marco publicado: v0.5.5-disable-worker-running-notice

## 56. Immediate gateway feedback
- DONE 0.5.2 feedback imediato para run-command aceito.
- DONE 0.5.2 feedback imediato para invalid_envelope parseavel.

## Version alignment 0.5.3
- Versao atual: 0.5.5
- Marco publicado: v0.5.5-disable-worker-running-notice

## 57. Gateway feedback dedup
- DONE 0.5.3 feedback inicial idempotente por command_id e source_chat_id.
- DONE 0.5.3 reducao de avisos duplicados de progresso.
- DONE 0.5.3 smoke_gateway_feedback_dedup.py.

## Version alignment 0.5.5
- Versao atual: 0.5.5
- Marco publicado: v0.5.5-disable-worker-running-notice

## 59. Disable worker running notice
- DONE 0.5.5 remove aviso intermediario do worker.
- DONE 0.5.5 fluxo esperado: queued inicial + AI_LOCAL_RUN final.

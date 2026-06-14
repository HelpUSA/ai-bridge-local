# AI Bridge Local - Queue triage playbook 0.4.88

## Objetivo
Definir um playbook seguro para triagem da fila local do watcher.

## Principios
- Nunca limpar queued, delivering, failed ou dead_letters sem snapshot previo.
- Primeiro auditar, depois classificar, depois propor acao.
- Preferir relatorios read-only antes de qualquer correcao.
- Separar invalid_messages de dead_letters.

## Ordem recomendada
1. Rodar queue_health_audit.
2. Verificar delivering antigo.
3. Listar queued commands.
4. Gerar amostra de failed e dead_letters.
5. Criar plano de limpeza dry-run.
6. Aplicar mudanca somente com aprovacao explicita.

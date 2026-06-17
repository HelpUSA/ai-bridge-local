# AI Bridge Local - Obsidian Knowledge Vault v1

Data: 2026-06-17
Modo: Markdown local
Risco: baixo

## Objetivo

Criar uma base de conhecimento local em Markdown, compativel com Obsidian, para registrar tarefas, decisoes, erros, smokes e releases do AI Bridge Local.

## Entregas

- knowledge/00_HOME.md
- knowledge/projects/ai-bridge-local/status.md
- knowledge/templates/task.md
- knowledge/templates/decision.md
- knowledge/templates/error.md
- knowledge/templates/smoke.md
- knowledge/templates/release.md
- knowledge/tasks/.gitkeep
- knowledge/decisions/.gitkeep
- knowledge/errors/.gitkeep
- knowledge/smokes/.gitkeep
- knowledge/releases/.gitkeep
- scripts/watcher/knowledge_writer.py
- scripts/watcher/smoke_knowledge_vault.py

## Politica

O vault nao deve armazenar segredos, tokens, credenciais ou dados sensiveis.

A funcao inicial e documentar conhecimento operacional, nao executar automacoes externas.

## Uso inicial

Abrir a pasta knowledge no Obsidian como vault.

O Smart Watcher podera gerar notas com:

```powershell
python scripts/watcher/knowledge_writer.py task --title "Minha tarefa" --body "Resumo" --tags "smart-watcher"
```

## Proximas atividades

1. Integrar knowledge_writer.py ao smart_task_runner.py.
2. Registrar automaticamente falhas parse_error em knowledge/errors.
3. Registrar releases em knowledge/releases.
4. Criar resumo executivo por tarefa.
5. Criar indice automatico por data.

# AI Bridge Local - Blocos da proxima fase 0.4.64

## Bloco 1 - API local read-only
- Criado local_api_readonly.py para leitura segura de metadados e preview de arquivos dentro do repo.
- Nao executa comandos e nao altera arquivos.

## Bloco 2 - API local dry-run
- Criado local_api_dry_run.py para planejar intents de leitura, escrita e comando sem executar.
- Toda mutacao futura exige aprovacao explicita.

## Bloco 3 - comunicacao entre chats
- Criado chat_bridge_plan.py com desenho de inbox, outbox, status e reconciliacao.
- A extensao passa a ser dependencia opcional depois que a API local estiver madura.

## Bloco 4 - validacao
- Criado smoke_local_api_foundations.py.
- Integrado ao release_check e validate_all.

## Proximos blocos sugeridos
- Implementar storage real da API local em modo read-only.
- Implementar endpoints locais com dry-run obrigatorio.
- Criar painel simples para status, fila e auditoria.

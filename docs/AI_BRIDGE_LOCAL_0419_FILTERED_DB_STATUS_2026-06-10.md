# AI Bridge Local 0.4.19 - filtered DB status

Data: 2026-06-10

## Objetivo

Separar melhor os relatórios operacionais do AI Bridge Local quando o mesmo queue_local.db contém comandos de outras frentes.

## Arquivo adicionado

- scripts/watcher/ai_bridge_local_filtered_db_status.py

## Uso principal

Relatório filtrado por prefixo padrão:

python scripts/watcher/ai_bridge_local_filtered_db_status.py

Relatório filtrado por conversation_id:

python scripts/watcher/ai_bridge_local_filtered_db_status.py --conversation v0418_temp_cleanup_db_reports

Relatório filtrado por source_chat_id:

python scripts/watcher/ai_bridge_local_filtered_db_status.py --source-chat-id 6a28b5fe-2bf8-83e9-82d5-4ebd2269b617

## Observação

O filtro padrão usa o prefixo ai_bridge_local_ no command_id. Isso reduz o ruído de comandos de outras aplicações registrados no mesmo banco local.

# AI Bridge Local 0.4.30 - parse e delivery feedback

## Objetivo

Fechar duas lacunas de feedback automatico:

- envelope invalido visivel no chat deve gerar resposta local mesmo quando created_at_utc estiver antigo;
- envio inter-chat que fica em delivering sem ack deve gerar retorno automatico ao chat de origem.

## Mudancas

- content_script.js atualizado para 0.4.30.
- Removida a supressao de envelope_parse_error baseada apenas em created_at_utc antigo.
- Mantida deduplicacao por command_id, tipo e hash no localStorage.
- Criado scripts/watcher/ai_bridge_local_delivery_feedback.py para detectar send-chat-message em delivering sem ack e inserir feedback ao source_chat_id.

## Caso que motivou

- check_mt5_001 nao entrou no queue_local.db porque falhou antes do gateway.
- O comando havia sido colado agora, mas continha created_at_utc antigo.
- A guarda antiga suprimia resposta automatica por considerar stale.

## Validacao esperada

- node --check extension/content_script.js deve passar.
- git diff --check deve passar.
- delivery feedback deve listar candidatos em dry-run sem duplicar feedback ja inserido.
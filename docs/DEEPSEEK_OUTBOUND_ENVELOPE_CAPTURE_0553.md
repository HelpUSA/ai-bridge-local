# DeepSeek outbound envelope capture 0.5.53

Data: 2026-06-19T11:45:53.401614

## Objetivo

Adicionar captura outbound de envelopes AI Bridge Local no chat.deepseek.com.

## Comportamento esperado

- ChatGPT -> DeepSeek continua usando rota direta ja existente.
- DeepSeek, ao responder com bloco local entre marcadores AI_BRIDGE_LOCAL_START e AI_BRIDGE_LOCAL_END, passa a ter o envelope capturado pelo content script.
- O envelope capturado e enviado ao background com type AI_BRIDGE_CAPTURED_ENVELOPE.
- O background valida source_chat_id, action e delivery_kind antes de publicar.
- A aba DeepSeek mostra aviso visual simples de enviado ou erro.
- Envelopes antigos existentes no carregamento inicial sao marcados e nao reenviados.
- source_chat_id_mismatch no ChatGPT fica deduplicado para reduzir ruido quando envelopes de outros chats aparecem colados no historico.

## Validacao manual

1. Recarregar extensao.
2. Recarregar DeepSeek.
3. Confirmar console:
   - DeepSeek outbound envelope observer installed
4. Pedir ao DeepSeek para responder com envelope local.
5. Confirmar aviso visual no DeepSeek:
   - [AI_LOCAL] DeepSeek watcher local
6. Confirmar chegada no chat alvo.

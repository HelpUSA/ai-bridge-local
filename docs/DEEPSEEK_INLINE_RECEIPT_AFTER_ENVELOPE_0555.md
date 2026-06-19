# DeepSeek inline receipt after envelope 0.5.55

Data: 2026-06-19T12:06:56.850041

## Objetivo

Fazer o recibo do watcher local aparecer visualmente logo depois do envelope gerado pelo DeepSeek.

## Problema observado

Na 0.5.54, a entrega DeepSeek -> ChatGPT funcionava, mas a confirmacao visual podia ficar ambigua: a mensagem recebida podia aparecer antes do ultimo envelope ou o recibo podia ficar em painel/posicao pouco clara.

## Comportamento esperado

Quando o DeepSeek gera um envelope outbound, a extensao deve:

1. Capturar o envelope.
2. Enviar ao background.
3. Receber retorno do background.
4. Inserir recibo persistente logo depois do elemento DOM que contem o envelope.
5. Usar painel fixo apenas como fallback quando nao conseguir achar o bloco do envelope.

## Recibo esperado em sucesso

[AI_LOCAL] DeepSeek watcher local
envelope capturado e entregue pela extensao
id=<command_id>
status=sent_direct ou accepted
versao=0.5.55
origem=<deepseek_chat_id>
destino=<target_chat_id>
observacao=Mensagem inter-chat enviada pelo watcher local.

## Validacao manual

1. Recarregar extensao.
2. Dar F5 no ChatGPT origem e no DeepSeek.
3. Confirmar console com [Local v0.5.55] Active.
4. Enviar probe DeepSeek reply back.
5. Confirmar que a resposta chega ao ChatGPT.
6. Confirmar que o recibo aparece abaixo do envelope no DeepSeek.

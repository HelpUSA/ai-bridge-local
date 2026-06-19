# DeepSeek persistent delivery receipt 0.5.54

Data: 2026-06-19T11:57:31.552489

## Objetivo

Adicionar recibo persistente e visivel na aba DeepSeek depois que um envelope outbound for capturado e entregue.

## Problema observado

Na 0.5.53, o DeepSeek ja conseguia gerar envelope local correto e o watcher local conseguia entregar a mensagem ao destino, mas a aba origem ficava sem uma confirmacao persistente. Isso criava incerteza operacional para o agente origem e para o operador.

## Comportamento esperado

Ao capturar um envelope local gerado pelo DeepSeek, a extensao deve mostrar aviso persistente com:

- id do comando
- status
- versao
- origem
- destino
- erro, se houver

## Resultado esperado em sucesso

[AI_LOCAL] DeepSeek watcher local
envelope capturado e entregue pela extensao
id=<command_id>
status=sent_direct ou accepted
versao=0.5.54
origem=<deepseek_chat_id>
destino=<target_chat_id>
observacao=Mensagem inter-chat enviada pelo watcher local.

## Validacao manual

1. Recarregar extensao.
2. Dar F5 no ChatGPT origem e no DeepSeek.
3. Confirmar console com [Local v0.5.54] Active.
4. Enviar probe DeepSeek reply back.
5. Confirmar que a resposta chega ao ChatGPT.
6. Confirmar que a aba DeepSeek mostra recibo persistente apos o envelope.

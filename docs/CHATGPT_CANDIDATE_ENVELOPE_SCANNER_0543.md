# AI Bridge Local 0.5.43 - ChatGPT candidate envelope scanner

Data: 2026-06-19T12:59:43.885178+00:00

## Objetivo

Corrigir captura de envelopes em respostas do ChatGPT quando a página já contém mensagens `[AI_LOCAL]`.

## Problema

O scanner global antigo lia `document.body.innerText` e podia ignorar a página inteira quando qualquer mensagem anterior continha `[AI_LOCAL]`, `[AI_LOCAL_ERRO]` ou `[AI_LOCAL_RUN]`.

## Mudança

- Ignora status local apenas quando o candidato começa com status local.
- Escaneia candidatos específicos: `article`, `pre`, `code`, `.markdown`, `[data-message-author-role]`.
- Adiciona varredura periódica e observer de mutações.
- Preserva roteamento 0.5.42:
  - inter-chat direto para `send-chat-message/inter_agent_message`
  - gateway obrigatório para `run-command/local_capability`

## Pós-instalação

Recarregar extensão e abas origem/destino.

# AI Bridge Local - Latency parallel polling architecture 0.4.98

## Objetivo
Documentar a arquitetura publicada em v0.4.97-latency-parallel-polling para polling rapido, paralelo e independente por chat.

## Como era antes
O background fazia um loop sequencial sobre os chats registrados. Cada chat aguardava fetch, injectText, ack e delivery status antes do proximo chat comecar. Como injectText podia esperar ate 20000 ms, um chat lento bloqueava todos os demais.

## Como ficou agora
- pollMessages cria um snapshot dos chatIds registrados.
- Cada chatId chama pollOneChat(chatId).
- Promise.allSettled executa os chats em paralelo logico.
- pollInFlight evita sobreposicao de ciclos de polling.
- perChatInFlight evita entrega duplicada no mesmo chat.
- Outros chats continuam processando mesmo quando um chat esta lento.
- MAX_ACTIONS_PER_CHAT_CYCLE limita cada chat a 3 acoes por ciclo.
- pollMessagesSoon agenda fast path com debounce de 150 ms apos startup, postCommand e registro do chat.

## Latencia esperada
- Fallback: ate cerca de 1000 ms para descobrir nova acao.
- Fast path: cerca de 150 ms mais tempo de gateway e injecao no tab ativo.
- Um chat lento fica isolado no proprio pollOneChat e nao segura a fila global.

## Escalabilidade
Chats adicionais entram no registry e recebem processamento independente por pollOneChat. A arquitetura remove a fila global bloqueante. Para centenas de chats, a proxima evolucao recomendada e um limite global de concorrencia, mantendo perChatInFlight por chat.

## Telemetria minima
- poll_started
- action_received
- inject_started
- inject_done
- ack_posted

## Compatibilidade
Os caminhos postAck e postDeliveryStatus continuam ativos nos fluxos acked e error.

# AI Bridge Local - Plano da proxima fase

## Frente A - controle direto sem watcher
- Desenhar API local propria para arquivos e comandos.
- Separar leitura, escrita e execucao em intents auditaveis.
- Comecar com modo read-only e dry-run.

## Frente B - comunicacao entre chats sem extensao
- Definir protocolo de mensagens entre sessoes HelpUSAI.
- Persistir caixa de entrada/saida em storage local.
- Criar reconciliacao de status acked, failed e delivering.

## Frente C - painel local
- Criar control center para fila, comandos, dead letters e releases.
- Mostrar auditoria curta pos-release.
- Expor relatorios sem depender de logs truncados.

## Frente D - governanca leve
- Manter operacao sem bloqueios excessivos.
- Adicionar blacklist opcional somente para comandos perigosos.
- Registrar aprovacao humana para acoes destrutivas.

## Ordem recomendada
1. API local read-only.
2. API local dry-run.
3. Execucao aprovada por envelope.
4. Painel de status.
5. Comunicacao entre chats.

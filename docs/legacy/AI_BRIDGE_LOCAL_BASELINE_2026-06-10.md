# AI Bridge Local - baseline operacional 2026-06-10

## Baseline fechado

Commit atual: 6262cde

Tag atual: v0.4.14-confirm-send-before-ack

Componentes validados:

- Extensao: AI Bridge Local 0.4.14
- Gateway local: gateway_local.py v0.2.1
- Worker local: brain_worker.py v0.1.2
- Banco local: queue_local.db
- Porta local: http://127.0.0.1:8766

## O que esta funcionando

- Envio inter-chat no mesmo perfil.
- Envio cross-profile entre perfis diferentes do navegador.
- Execucao local via run-command.
- Retorno de stdout, stderr e return_code para o chat via [AI_LOCAL_RUN].
- ACK de envio somente apos confirmacao real no composer desde a versao 0.4.14.
- Gateway aceitando payload.command, payload.cwd e payload.timeout_seconds.

## Commits e tags importantes

- 2786c2b / v0.3.8-interchat-baseline: baseline inter-chat inicial.
- 12acc6a / v0.3.8-run-command-smoke: smoke inicial de run-command.
- a25073e / v0.4.13-local-run-command-0.2.1: extensao 0.4.13, gateway 0.2.1, worker 0.1.2.
- 6262cde / v0.4.14-confirm-send-before-ack: confirmacao real de envio antes de ACK.

## Fluxos validados

Inter-chat:

Chat origem -> extensao -> gateway local -> chat destino -> extensao -> composer -> envio.

Cross-profile:

Perfil A do navegador -> gateway local comum -> perfil B do navegador.

Run-command local:

Chat -> extensao -> gateway local -> worker -> processo local -> ACK -> mensagem [AI_LOCAL_RUN] de retorno ao chat.

## Correcoes importantes

### payload_json vazio

O gateway gravava apenas body.payload, mas alguns envelopes mandavam command, cwd e timeout_seconds no topo.

Correcao: gateway_local.py v0.2.1 normaliza command, cwd, timeout_seconds e env para dentro de payload.

### WinError 87

O worker recebia payload vazio, montava cmd=[] e chamava subprocess.run([]).

Correcao: brain_worker.py v0.1.2 rejeita comando ausente com erro claro e aceita payload.command como array ou string.

### ACK falso

A extensao marcava ACK logo apos clicar no botao, mesmo se o composer continuasse preenchido aguardando Enter manual.

Correcao: extensao 0.4.14 so marca ACK quando o composer limpa ou quando o texto original some do composer.

## Observacao pendente

Foi observada duplicacao visual ocasional de mensagens [AI_LOCAL] no chat atual.

O banco nao mostrou duplicata real de command_id. Enquanto nao houver duplicata real no banco, tratar como problema visual/status, nao como duplicacao de fila.

## Recarregamento obrigatorio

Apos alterar qualquer arquivo abaixo, recarregar a extensao em chrome://extensions nos dois perfis e dar F5 nas abas de chat:

- extension/background.js
- extension/content_script.js
- extension/manifest.json

## Diagnostico rapido

- queued: comando ainda nao foi entregue ao destino.
- delivering: destino pegou, mas ainda nao confirmou ACK.
- acked: destino confirmou.
- failed: consultar stderr e last_error.

## Regra de seguranca

Nao considerar um fluxo aprovado apenas porque apareceu [AI_LOCAL]. Verificar tambem:

- se o destino recebeu;
- se o banco marcou acked;
- se nao houve duplicata real de command_id;
- se o retorno trouxe method coerente, como button_click_confirmed ou enter_confirmed.

# AI Bridge Local 0.4.17 - visual dedupe e temp-script workflow

## Objetivo

Fechar a frente 0.4.17 com duas melhorias pequenas e seguras sobre o baseline 0.4.16:

- reduzir duplicidade visual dos status compactos `[AI_LOCAL]` e `[AI_LOCAL_ERRO]`;
- permitir execução de scripts temporários por `run-command` sem depender de comandos grandes inline em JSON.

## Baseline

- Baseline anterior: commit `43b61d5`
- Tag anterior: `v0.4.16-submit-recovery`
- Escopo exclusivo: `D:/dev/autocode/ai-bridge-local`

## Mudança 1: visual-dedupe

O `background.js` já tinha dedupe em memória por chave `command_id:status`. A versão 0.4.17 complementa isso removendo `Date.now()` do `command_id` gerado para mensagens compactas de status local.

Antes, a mensagem de status era sempre inserida com um identificador único por timestamp, o que facilitava duplicidade visual se o mesmo status fosse reemitido.

Agora, o `command_id` do status compacto é estável por comando e status:

`local_status_delivery_<status>_<command_id_original>`

Isso permite que a restrição `UNIQUE` do banco local ajude a rejeitar duplicatas, além do dedupe em memória já existente.

## Mudança 2: temp-script workflow

O `brain_worker.py` agora aceita, dentro do payload de `run-command`:

- `script_text`: conteúdo do script temporário;
- `script_ext`: extensão do script, como `.ps1` ou `.py`;
- `command`: opcional. Se ausente, o worker escolhe o executor com base na extensão.

Quando `script_text` é informado, o worker grava o arquivo em:

`temp/watcher_scripts/<command_id>.<ext>`

Depois executa o script temporário. Isso evita envelopes JSON frágeis com comandos longos, aspas, barras invertidas e blocos inline grandes.

## Compatibilidade

- O formato antigo `payload.command` continua funcionando.
- O novo fluxo é opt-in: só ativa quando existe `script_text`.
- Não muda schema do banco.
- Não muda gateway local.

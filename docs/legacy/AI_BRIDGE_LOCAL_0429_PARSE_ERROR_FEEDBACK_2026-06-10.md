# AI Bridge Local 0.4.29 - parse error feedback

Data: 2026-06-10

## Objetivo

Melhorar o retorno para chats que enviam envelopes locais invalidos.

Antes, quando o JSON entre os marcadores locais nao podia ser parseado, o emissor recebia uma mensagem generica. A partir da 0.4.29, o retorno explica que nada foi executado e orienta como reenviar corretamente.

## Novo comportamento

Para `envelope_parse_error`, a extensao passa a incluir:

- `executado=nao`
- `causa_provavel`
- `correcao`
- `modelo_seguro`
- observacao de seguranca para comandos de limpeza, move ou delete

## Casos detectados

- aspas curvas/Unicode em vez de aspas JSON validas
- caracteres invisiveis/zero-width
- texto quebrado letra por letra
- quebra de linha dentro de string JSON sem escape
- comando inline grande/fragil
- JSON incompleto, aspas ou backslashes nao escapados

## Motivacao

Um chat externo enviou o comando `clean_temp_files_001` corrompido por quebras artificiais, aspas curvas e trechos soletrados verticalmente. Esse tipo de envelope nao deve travar o fluxo silenciosamente: o chat emissor precisa receber instrucao clara de que nada foi executado e de como reenviar.

## Validacao

- `node --check extension/content_script.js`
- `git diff --check`

# AI Bridge Local - Watcher failure taxonomy 0.4.89

## Objetivo
Catalogar erros recorrentes do watcher e a resposta segura para cada classe.

## Classes de falha
- envelope_parse_error: JSON invalido, aspas internas, escapes ou payload inline grande.
- indentation_loss: Python escrito por array ou here-string perdeu indentacao.
- bom_version_mismatch: VERSION salvo com BOM e smoke_docs le versao com caractere invisivel.
- output_truncated: push ou release_check concluiu, mas o fim do log nao apareceu.
- queue_stale_delivering: comando aparece como delivering durante a propria execucao ou ficou antigo.
- crlf_warning: aviso de LF para CRLF sem falha de release.

## Respostas seguras
- Para parse: dividir comando e evitar aspas duplas internas.
- Para indentacao: escrever Python via Base64.
- Para BOM: salvar arquivos criticos com UTF-8 sem BOM.
- Para truncamento: rodar audit final read-only.
- Para fila: rodar queue_health_audit antes de qualquer limpeza.
- Para CRLF: tratar como aviso se checks e commit passarem.

# AI Bridge Local - Safe envelope templates 0.4.85

## Objetivo
Padronizar envelopes seguros para comandos watcher longos.

## Regras
- Preferir blocos pequenos.
- Evitar python -c em script_text.
- Evitar aspas duplas internas no script_text.
- Evitar regex com barra invertida em JSON inline.
- Usar Base64 para arquivos Python com indentacao sensivel.
- Separar escrita, validacao, commit e auditoria.

## Checklist
- Escrever arquivos.
- Rodar smoke especifico.
- Atualizar versao e guia.
- Rodar release_check.
- Commit, tag, push.
- Rodar audit final read-only.

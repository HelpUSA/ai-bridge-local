# AI Bridge Local - Release safety checklist 0.4.87

## Objetivo
Consolidar o checklist seguro de release do AI Bridge Local.

## Checklist obrigatorio
- Confirmar arvore limpa antes de iniciar.
- Escrever arquivos em bloco separado.
- Rodar smoke especifico.
- Atualizar VERSION, manifest, scripts JS e guia.
- Rodar smoke_docs e smoke_version_alignment.
- Rodar git diff --check.
- Rodar release_check.
- Commitar somente depois dos checks.
- Criar tag anotada.
- Fazer push de branch e tag.
- Rodar audit final read-only.

## Regras anti-parser
- Preferir comandos pequenos.
- Evitar aspas duplas internas em script_text.
- Usar Base64 para Python com indentacao sensivel.
- Separar escrita, preparacao e fechamento.

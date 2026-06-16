# Safe release runner 0.5.15

Objetivo: criar um runner PowerShell reutilizavel para releases locais seguras.

## Problema resolvido

Scripts PowerShell extensos podem continuar apos falhas de comandos externos quando nao verificam explicitamente o codigo de retorno.
Isso causou o micro 0.5.13 ser commitado e enviado mesmo com validacoes falhando.

## Solucao

O arquivo scripts/release/run_safe_release.ps1 fornece:

- Invoke-Native para comandos externos sem encerrar o shell.
- Assert-NoBomVersion para impedir VERSION com UTF-8 BOM.
- ValidationCommands obrigatorios antes e depois do commit.
- AddPaths explicitos para evitar commit amplo acidental.
- Push opcional.
- Tag opcional.

## Regra operacional

Todo script completo de release deve usar checagem explicita do codigo de retorno.
Arquivos de versao devem ser escritos em UTF-8 sem BOM.
Este micro nao executa entrega inter-chat.
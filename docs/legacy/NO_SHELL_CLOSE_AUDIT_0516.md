# No shell close audit 0.5.16

Objetivo: proteger scripts PowerShell versionados contra comandos que encerram o shell interativo do operador.

## Motivacao

Durante a evolucao 0.5.15, um comando de encerramento de processo em script interativo fechou o shell local.
A partir deste micro, scripts versionados devem falhar com throw ou checagem por funcao, preservando o shell aberto.

## Regra operacional

- Scripts PowerShell interativos devem usar throw para interromper fluxo.
- Comandos nativos devem ser envolvidos por Invoke-Native ou funcao equivalente.
- Arquivos de versao devem continuar em UTF-8 sem BOM.
- Releases devem continuar com validacoes antes e depois de commit.
- Este micro nao executa entrega inter-chat.

## Arquivo principal

- scripts/watcher/smoke_no_shell_close_audit_0516.py
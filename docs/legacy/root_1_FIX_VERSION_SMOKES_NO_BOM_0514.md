# Fix version smokes and UTF-8 no BOM 0.5.14

Objetivo: corrigir por fix-forward as falhas introduzidas no micro 0.5.13.

## Problemas corrigidos

- VERSION havia sido gravado com BOM em ambiente PowerShell, causando leituras como \ufeff0.5.13.
- smoke_delivery_diagnostics_0512.py estava fixado em VERSION == 0.5.12 e falhava em versoes futuras.
- smoke_delivery_diagnostic_classifier_0513.py estava fixado em VERSION == 0.5.13 e falhava em versoes futuras.
- O script de release anterior nao interrompeu apos falhas de validacao porque comandos externos exigem checagem explicita de exit code.

## Regra operacional

Scripts completos devem usar funcao de execucao que interrompa em qualquer exit code diferente de zero.
Arquivos de versao devem ser gravados em UTF-8 sem BOM.
Este micro nao executa entrega inter-chat.
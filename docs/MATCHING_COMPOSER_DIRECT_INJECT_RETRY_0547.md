# AI Bridge Local 0.5.47 - Matching composer direct inject retry

Data: 2026-06-19T13:20:50.949357+00:00

## Problema

A rota direta inter-chat já capturou e tentou entregar, mas falhou com:

`composer_not_empty_before_inject`

O preview mostrou que o composer do destino já continha exatamente a mensagem que a extensão tentava enviar.

## Correção

- Mantém a trava para não sobrescrever texto manual.
- Se o composer já contém exatamente o mesmo texto solicitado pela extensão, trata como texto stale/owned.
- Limpa o composer e tenta a injeção novamente.
- Mantém feedback visível `[AI_LOCAL]` ou `[AI_LOCAL_ERRO]`.
- Mantém gateway obrigatório para `run-command/local_capability`.

## Observação

Isso não permite sobrescrever texto diferente. Só libera quando o conteúdo é exatamente igual ao texto que seria injetado.

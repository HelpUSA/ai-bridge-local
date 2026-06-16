# Release runner self-smoke 0.5.18

Objetivo: validar estaticamente que o runner de release contem protecoes essenciais antes de ser usado em batches maiores.

## Garantias verificadas

- Existe scripts/release/run_safe_release.ps1.
- O runner contem Invoke-Native.
- O runner contem Assert-NoBomVersion.
- O runner exige AddPaths explicitos.
- O runner executa validacoes.
- O runner executa git diff --check.
- O runner usa throw para falhas.
- Este micro nao executa entrega inter-chat.
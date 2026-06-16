# Release checklist 0.5.19

Objetivo: consolidar um checklist operacional para releases seguros do AI Bridge Local.

## Checklist obrigatorio

1. Confirmar branch limpa antes do patch.
2. Buscar baseline remoto com fetch.
3. Validar smokes historicos.
4. Atualizar VERSION em UTF-8 sem BOM.
5. Atualizar extension/manifest.json com name e version alinhados.
6. Criar ou atualizar documentacao do micro.
7. Criar ou atualizar smoke do micro.
8. Tornar smoke anterior forward-compatible quando aplicavel.
9. Rodar smoke_all.py ou lista completa de smokes.
10. Rodar smoke_version_alignment.py.
11. Rodar smoke_docs.py.
12. Rodar git diff --check.
13. Usar git add com caminhos explicitos.
14. Criar commit unico e tag unica.
15. Revalidar apos commit.
16. Fazer push de main e tag.
17. Confirmar status final limpo.

## Regras permanentes

- Nao usar comando que encerra shell em scripts interativos.
- Nao gravar VERSION com BOM.
- Nao executar entrega inter-chat sem autorizacao explicita.
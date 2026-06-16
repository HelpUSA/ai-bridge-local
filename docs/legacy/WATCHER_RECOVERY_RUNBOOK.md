# AI Bridge Local - Watcher recovery runbook 0.4.91

## Objetivo
Converter a taxonomia de falhas do watcher em passos operacionais de recuperacao.

## Quando usar
- Apos envelope_parse_error.
- Apos indentation_loss em scripts Python.
- Apos bom_version_mismatch em VERSION ou smoke_docs.
- Apos output_truncated em release com push ou tag.
- Apos queue_stale_delivering ou crescimento de dead_letters.

## Procedimento seguro
1. Nao repetir o mesmo comando grande.
2. Rodar audit read-only curto.
3. Classificar a falha pela taxonomia.
4. Preparar comando minimo de correcao.
5. Para Python sensivel a indentacao, usar Base64.
6. Para BOM, regravar arquivo com UTF-8 sem BOM.
7. Para truncamento, validar HEAD, tag, VERSION, guia e smokes.
8. Para fila, usar queue_health_audit antes de qualquer limpeza.

## Resultado esperado
Cada falha deve produzir uma correcao pequena, auditavel e sem mudanca destrutiva implicita.

# DeepSeek inline receipt syntax repair 0.5.56

Data: 2026-06-19T12:16:29.624779

## Objetivo

Corrigir a 0.5.55, que foi commitada com erro de sintaxe JavaScript apesar do node --check ter falhado.

## Problema

O trecho formatReceiptLines ficou com string quebrada:

return (lines || []).filter(Boolean).join("
");

Isso impede o content_script.js de carregar.

## Correcao

A 0.5.56 repara o literal para:

return (lines || []).filter(Boolean).join("\\n");

Tambem valida a linha:

receipt.textContent = title + "\\n" + formatReceiptLines(lines);

## Observacao operacional

A tag 0.5.55 foi publicada, mas deve ser considerada superseded pela 0.5.56.

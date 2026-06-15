# AI Bridge Local - Latency parallel polling report 2026-06-14

## Status
Resolvido, validado e publicado.

## Publicacao validada
- Commit auditado: ffbfbc6
- Tag: v0.4.97-latency-parallel-polling
- VERSION e manifest alinhados em 0.4.97 no audit final.
- Guia compactado de 169 MB para 15.835 bytes antes do push final.

## Resultado tecnico
- Polling fallback reduzido de 5000 ms para 1000 ms.
- Registro de chat reduzido de 5000 ms para 1500 ms.
- Chats processados via pollOneChat com Promise.allSettled.
- perChatInFlight protege contra duplicidade no mesmo chat.
- Um chat lento nao bloqueia os demais.
- Drenagem por chat limitada a 3 acoes por ciclo.
- Fast path com pollMessagesSoon em 150 ms.

## Validacoes
- node --check extension/background.js
- node --check extension/content_script.js
- smoke_latency_parallel_polling.py
- smoke_docs.py
- smoke_version_alignment.py
- git diff --check
- release_check.ps1

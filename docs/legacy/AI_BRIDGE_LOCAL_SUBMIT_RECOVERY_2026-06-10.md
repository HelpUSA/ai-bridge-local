# AI Bridge Local submit recovery 0.4.16

Status: patch local aplicado, sem commit, sem tag e sem deploy.

Arquivos alterados: extension/manifest.json, extension/background.js, extension/content_script.js.

Causa raiz: o content_script podia confirmar envio usando documentContainsSentMessage quando o composer ainda continha texto. Isso podia gerar falso button_click_confirmed e status acked com texto preso no composer.

Correcao conservadora: isSubmitted agora so retorna true quando o composer fica vazio. Se ainda houver texto no composer, o envio nao e confirmado.

Validacoes executadas: node --check em background e content_script, python -m py_compile em gateway_local.py e brain_worker.py, git diff --check, run-command smoke, cross-profile positivo curto.

Resultado observado: validacoes OK e cross-profile positivo apos patch retornou acked.

Pendencias antes de commit: testar caso negativo com composer ocupado antes da injecao, testar caso de texto preso apos tentativa de envio, verificar mapping ok false para failed no background, revisar duplicacao visual em ciclo separado.

Recomendacao: nao commitar ate os testes negativos confirmarem composer_not_empty_before_inject e submit_not_confirmed_composer_still_has_text.

Confirmacao adicional: background.js mapeia result.ok true para acked e result.ok false para failed. A correcao principal fica no content_script.js, impedindo ok true quando o composer ainda contem texto.

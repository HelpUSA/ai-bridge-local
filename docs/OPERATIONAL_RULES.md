# AI Bridge Local - regras operacionais

Atualizado em 2026-06-12.

## Regras obrigatorias

1. Auditar a extensao antes de considerar o sistema normalizado.
2. Sempre versionar a numeracao quando alterar extensao, gateway, worker, Control Center, self-heal ou scripts operacionais.
3. Nao abrir mais de um brain_worker.py real por padrao.
4. Se aparecer worker duplicado, usar scripts/watcher/self_heal.py --apply ou o supervisor seguro.
5. Nao apagar linhas do queue_local.db em limpeza automatica; preferir marcar como failed e registrar evento.
6. Antes de qualquer self-heal com --apply, fazer backup do queue_local.db.
7. Nao matar processos globais de python, node, git, powershell ou cmd.
8. Para parar processo, filtrar por caminho exato do projeto e script esperado.
9. Nao remover .git/index.lock sem verificar processos git ativos.
10. Para scripts grandes, usar script_text/script_ext ou arquivo real; evitar comandos inline gigantes.
11. Evitar python -c grande.
12. Evitar JSON cru dentro de message.
13. Usar delivery_kind inter_agent_message para mensagens entre chats.
14. Usar delivery_kind local_capability para run-command local.
15. Recarregar extensao e dar F5 nos chats antes de smoke operacional completo.

## Checklist de saude

- git status -sb precisa estar limpo antes de novas alteracoes.
- python scripts/watcher/health_check.py deve rodar sem erro.
- python scripts/watcher/self_heal.py --dry-run deve mostrar gateway_count=1 e worker_count=1.
- commands nao deve ter queued ou delivering antigos.
- python scripts/watcher/smoke_robustness.py deve retornar ROBUSTNESS_SMOKE_OK.
- node --check extension/content_script.js deve passar.
- node --check extension/background.js deve passar.
- git diff --check deve passar.

## Checklist de extensao

- Conferir extension/manifest.json.
- Conferir extension/content_script.js.
- Conferir extension/background.js.
- Conferir versao nos tres pontos.
- Conferir host_permissions e content_scripts para chatgpt.com e ai.helpusbr.com.
- Conferir parser dos marcadores @@AI_BRIDGE_LOCAL_START@@ e @@AI_BRIDGE_LOCAL_END@@.
- Conferir normalizacao de local_inter_agent_message para inter_agent_message.
- Conferir envio para gateway local.
- Conferir postDeliveryStatus e mensagens de erro.

## Versionamento

Ao alterar qualquer parte operacional, incrementar versao compatível:

- Extensao: manifest.json, content_script.js e background.js.
- Worker: constante VERSION em brain_worker.py.
- Gateway: constante VERSION em gateway_local.py se existir.
- Self-heal: constante VERSION em scripts/watcher/self_heal.py.
- Docs: registrar no guia ou status operacional.

## Recuperacao automatica esperada

O sistema deve tender a auto-recuperacao:

- Gateway ausente: self-heal deve iniciar.
- Worker ausente: self-heal deve iniciar.
- Worker duplicado: self-heal deve manter o mais antigo e parar duplicados.
- Delivering antigo: self-heal deve marcar failed e registrar evento.
- Queued legado/smoke antigo: self-heal deve marcar failed e registrar evento.

## Ordem padrao de operacao

1. health_check.py.
2. self_heal.py --dry-run.
3. self_heal.py --apply se houver candidatos seguros.
4. smoke_robustness.py.
5. auditoria da extensao.
6. incremento de versao quando houver alteracao.
7. commit pequeno.
8. push normal, sem force.

## HelpUSAI

- HelpUSAI / ai.helpusbr.com é alvo oficial da extensão e deve ser auditado junto com ChatGPT.
- Toda auditoria da extensão deve conferir ChatGPT e HelpUSAI.
- Toda alteração de versão da extensão deve manter manifest, content_script e background alinhados.

# AI Bridge Local 0.5.42 - Direct inter-chat router safe

Data: 2026-06-19T02:10:10.703445+00:00

## Objetivo

Permitir conversa simples entre chats sem gateway/DB, preservando o fluxo gateway/worker para comandos locais.

## Regras de roteamento

### Direto pela extensão

Usar rota direta somente quando todos os critérios forem verdadeiros:

- `action = send-chat-message`
- `delivery_kind = inter_agent_message`
- `target_chat_id` está registrado em aba aberta
- `force_gateway`, `audit_required`, `persist_required` e `require_gateway` não estão ativos

### Gateway obrigatório

Sempre usar gateway/DB/worker quando:

- `action = run-command`
- `delivery_kind = local_capability`
- `force_gateway = true`
- `audit_required = true`
- `persist_required = true`
- `require_gateway = true`

## Avisos e segurança

- A rota direta não faz fallback automático para o gateway.
- Se a aba destino não estiver registrada, o background retorna `target_chat_not_registered`.
- O content script de origem deve exibir aviso ao usuário quando a rota direta falhar.
- O fluxo gateway existente, incluindo queued, acks e AI_LOCAL_RUN, permanece inalterado.

## Pós-instalação

Recarregar a extensão e recarregar as abas de origem e destino.

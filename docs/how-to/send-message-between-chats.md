---
type: how-to
status: draft
tags:
  - how-to
  - interchat
---

# Send message between chats

## Procedimento atual: gateway-first

Toda comunicação operacional entre chats segue o modelo gateway-first.

1. Delimite o envelope com `@@AI_BRIDGE_LOCAL_START@@` e `@@AI_BRIDGE_LOCAL_END@@`.
2. Use JSON estrito, mantenha `source_chat_id` igual ao chat atual e use um `command_id` novo em cada tentativa.
3. Envie o envelope ao gateway por `POST /bridge/commands`.
4. Para mensagens entre chats, use `action: send-chat-message`, `type: send-chat-message` e `delivery_kind: inter_agent_message`.
5. Para execução local, use `action: run-command`, `type: run-command`, `delivery_kind: local_capability` e `target_chat_id: gateway-brain-supervisor`.
6. Registre acknowledgements de entrega por `POST /bridge/acks`.
7. Trate `queued` e o acknowledgement de entrega como estados intermediários. Quando a operação depender de stdout ou stderr, aguarde o evento `AI_LOCAL_RUN` com `result_is_final: 1`.
8. Use `force_gateway: true` quando o fluxo precisar passar explicitamente pelo gateway.
9. Não selecione `direct_interchat` nem `talk-inter-chat`; esses caminhos são legados ou desativados.

## Objetivo

Enviar mensagens entre chats pelo gateway local, com persistencia,
acknowledgement e diagnostico.

## Rota esperada

`send-chat-message` deve usar `local_gateway` e entrar por
`POST /bridge/commands`. `direct_interchat` e `talk-inter-chat` nao sao rotas
operacionais atuais.

<!-- AI_BRIDGE_MANAGED:INTERCHAT_AND_LOCAL_CAPABILITY:START -->

## Interchat messages and controlled local capabilities

### Canonical message envelope

Every attempt must use a unique `command_id`. A corrected retry must not reuse
an identifier that already failed parsing, validation, delivery, or execution.

Required fields include `schema`, `schema_version`, `command_id`, `action`,
`type`, `source_chat_id`, `target_chat_id`, `delivery_kind`,
`conversation_id`, `force_gateway`, and `no_reply`.

### Complex payloads

For long messages, nested JSON, multiline code, or many backslashes and quotes,
serialize the envelope programmatically and submit it to
`http://127.0.0.1:8766/bridge/commands`. This avoids browser scanner corruption
while preserving gateway, queue, watcher, and browser delivery.

A watcher-mediated response must persist the responding `source_chat_id`, the
intended `target_chat_id`, a new `command_id`, the expected message, and a
successful state.

### Read-only directory listing

A browser AI must request local filesystem work through
`gateway-brain-supervisor` with `delivery_kind=local_capability`.

Example target: `D:\dev\ai\docs`.

A safe request may list names, types, sizes, and modification timestamps. It
must not create, edit, rename, delete, or read file contents unless that access
is explicitly authorized.

Checklist:

1. Confirm the active source conversation.
2. Confirm `gateway-brain-supervisor` as destination.
3. Confirm the intended path.
4. Confirm read-only behavior or obtain write authorization.
5. Use a finite timeout and argument array.
6. Wait for the final executor result.
7. Inspect `return_code`, stdout, and stderr.
8. Verify that protected files and repository state did not change.

### Diagnostics

- `queued`: gateway acceptance only.
- `acked`: browser delivery acknowledgement only.
- `AI_LOCAL_RUN` with `result_is_final=1`: local execution finished.
- `envelope_parse_error`: strict JSON failed before the gateway.
- `source_chat_id_mismatch`: declared source differs from the active page.

Until ChatGPT scanner consolidation is complete, prefer direct gateway
submission for large or complex payloads.

<!-- AI_BRIDGE_MANAGED:CHATGPT_RUNTIME_OPERATION:START -->

### ChatGPT runtime operation

Only the primary ChatGPT outbound capture is active during normal
operation.

Registration cannot run concurrently and uses a minimum interval of
30 seconds for an unchanged conversation URL.

Unavailable heartbeat capability is skipped before delivery.

After updating the extension:

1. reload the unpacked extension;
2. reload the ChatGPT and HelpUS conversations;
3. confirm that only the primary ChatGPT scanner is installed;
4. confirm that registration messages no longer repeat rapidly;
5. confirm that heartbeat-unavailable messages no longer repeat;
6. execute one unique interchat smoke test;
7. execute one read-only local-capability smoke test.

<!-- AI_BRIDGE_MANAGED:CHATGPT_RUNTIME_OPERATION:END -->

<!-- AI_BRIDGE_MANAGED:COORDINATED_VERSION_0_5_84:START -->

## Version 0.5.85 activation

After applying the coordinated version update:

1. reload the unpacked browser extension;
2. restart the gateway process;
3. restart worker, runner, and watcher processes;
4. close and reopen the Control Center;
5. confirm the Control Center title reports `0.5.85`;
6. confirm the gateway health response reports `0.5.85`;
7. execute one interchat smoke test;
8. execute one read-only local-capability smoke test.

A running process may continue reporting `0.5.83` until it is
restarted. This does not mean the source update failed.

<!-- AI_BRIDGE_MANAGED:COORDINATED_VERSION_0_5_84:END -->

<!-- AI_BRIDGE_MANAGED:INTERCHAT_AND_LOCAL_CAPABILITY:END -->

<!-- AI_BRIDGE_MANAGED:COMPACT_GATEWAY_COMMANDS_0585:START -->

## Compact commands 0.5.85

Restart gateway and worker, reload the extension, then run `python scripts/smoke/smoke_gateway_command_plane_0585.py`.

See `docs/how-to/compact-gateway-commands.md`.

<!-- AI_BRIDGE_MANAGED:COMPACT_GATEWAY_COMMANDS_0585:END -->

<!-- AI_BRIDGE_MANAGED:CURRENT_GATEWAY_FIRST_PROCEDURE_0585:START -->

## Current transport boundary

Inter-agent browser messages use the gateway transport on port `8766` and enter
through `POST /bridge/commands`.

The compact command plane on port `8767` is additive. It does not restore
extension-owned direct dispatch.

`queued` means gateway acceptance. Browser delivery requires acknowledgement.
A local capability that produces output is complete only after the final
`AI_LOCAL_RUN` result.

<!-- AI_BRIDGE_MANAGED:CURRENT_GATEWAY_FIRST_PROCEDURE_0585:END -->

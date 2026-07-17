---
type: explanation
status: draft
tags:
  - architecture
  - router
---

# Extension router

## Modelo atual de roteamento: gateway-first

- A rota operacional ativa é `local_gateway`.
- O gateway local é o proprietário do plano de controle: classifica comandos, escolhe o plano de entrega e registra as transições de estado.
- Comandos entram por `POST /bridge/commands`.
- Confirmações de entrega são registradas por `POST /bridge/acks`.
- A ação `run-command` usa `delivery_kind: local_capability` e `target_chat_id: gateway-brain-supervisor`; quando houver saída esperada, a conclusão depende do evento final `AI_LOCAL_RUN`.
- `direct_interchat` e `talk-inter-chat` são rotas legadas ou desativadas e não devem ser selecionadas como caminhos operacionais atuais.
- A extensão do navegador permanece fina: pode executar ações de navegador decididas pelo gateway, mas não é proprietária da classificação de rota nem pode contornar o plano de controle.

Descrições históricas mantidas adiante registram a evolução da implementação e não substituem este modelo atual.

## Responsabilidade

A extensão do navegador atua como adaptador fino. Ela executa apenas ações de navegador determinadas pelo gateway local. A classificação da rota, a escolha do plano de entrega e o registro das transições de estado pertencem ao gateway.

O router da extensão não deve selecionar `direct_interchat`, `talk-inter-chat` nem qualquer caminho paralelo. Comandos seguem por `local_gateway`, entram em `POST /bridge/commands` e usam `POST /bridge/acks` para acknowledgements de entrega.

## Principios

- O router decide rota.
- Apps executam a rota.
- Adapters conhecem cada IA.
- Gateway local executa comandos locais.

## Rotas principais

- direct_interchat: conversa entre abas.
- local_gateway: execucao via gateway local.

<!-- AI_BRIDGE_MANAGED:PLATFORM_ROUTING_AND_CAPABILITIES:START -->

## Platform routing, outbound capture, and local capabilities

This managed section records the platform-routing architecture validated during
the HelpUS AI integration work.

### Routing flow

1. The content script identifies the platform and active conversation.
2. The conversation is registered with the local gateway.
3. A platform adapter observes assistant-generated output.
4. A complete AI Bridge envelope is extracted as strict JSON.
5. `source_chat_id` is checked against the active conversation.
6. `command_id` is deduplicated.
7. The content script sends `AI_BRIDGE_CAPTURED_ENVELOPE` to the background worker.
8. The background worker routes the command to `/bridge/commands`.
9. The gateway persists it in `queue_local.db`.
10. A browser worker or `gateway-brain-supervisor` processes it.

### Platform adapters

| Platform | Conversation recognition | Assistant-output capture | State |
| --- | --- | --- | --- |
| ChatGPT | Conversation UUID in the URL | Primary outbound capture | Primary active; legacy scanners disabled by default |
| Gemini | Gemini routing rules | Gemini-specific observer | Implemented |
| DeepSeek | DeepSeek routing rules | DeepSeek-specific observer | Implemented |
| HelpUS AI | `/c/<uuid>` on `ai.helpusbr.com` | `article .markdown-message` | Implemented in working tree |

### HelpUS adapter

`installAiBridgeHelpUsCapturedEnvelopeBridge`:

- runs only on `ai.helpusbr.com`;
- extracts the chat UUID from `/c/<uuid>`;
- scans `article .markdown-message`;
- rejects blue user-message articles;
- supports streaming through `MutationObserver`;
- ignores historical envelopes during bootstrap;
- rejects incomplete or invalid JSON;
- verifies `source_chat_id`;
- deduplicates by `command_id`;
- forwards accepted commands as `AI_BRIDGE_CAPTURED_ENVELOPE`.

A whole-page scanner must not be used because incoming instructions may contain
envelope markers and could be recaptured.

### Delivery kinds

`inter_agent_message` sends to another registered browser conversation.

`local_capability` requests controlled local work from
`gateway-brain-supervisor`. A browser AI does not access the workstation
filesystem directly.

### Local capability safety

- Use a unique `command_id`.
- Declare `action`, `type`, working directory, and finite timeout.
- Prefer an argument array instead of shell interpolation.
- Treat read and write access as different authorization classes.
- Do not create, edit, rename, or delete files without authorization.
- Bound potentially large stdout and stderr.
- Record source, destination, command, status, and result.
- Reject a source chat that differs from the emitting page.

### Lifecycle

| Event | Meaning |
| --- | --- |
| `queued` | Gateway accepted and persisted the command |
| `acked` | Browser destination acknowledged delivery |
| `AI_LOCAL_RUN` | Local executor produced a final result |
| `return_code=0` | Local process completed successfully |
| `AI_LOCAL_ERRO` or `failed` | Validation, delivery, or execution failed |

`queued` does not prove browser delivery. `acked` does not prove a later local
command executed.

### Remaining technical work

1. Add runtime regression tests for the consolidated ChatGPT primary capture path.
2. Prevent partial or duplicate capture during streaming.
3. Debounce repeated conversation registration.
4. Implement or remove the inactive heartbeat interval.
5. Deduplicate repeated local status notifications.
6. Extract shared parser, validator, dedupe, and forwarding logic.
7. Add unit and end-to-end tests for all supported platforms.
8. Complete the HelpUS read-only `run-command` test.

<!-- AI_BRIDGE_MANAGED:CHATGPT_RUNTIME_STABILITY:START -->

### ChatGPT runtime stability

Normal operation uses the primary ChatGPT outbound capture as the
authoritative scanner.

The legacy scanners return before observers or intervals unless
explicitly enabled for diagnostics.

Conversation registration is non-concurrent and uses a minimum
interval of 30 seconds for an unchanged conversation URL.

The heartbeat callback returns before delivery when
`sendChatHeartbeat` is unavailable.

Validation includes three idempotence passes, pre-write JavaScript
syntax validation, all extension JavaScript checks, JSON parsing,
package discovery, protected hashes, and Git diff checks.

Reload the extension and run browser interchat plus read-only
local-capability smoke tests before release.

<!-- AI_BRIDGE_MANAGED:CHATGPT_RUNTIME_STABILITY:END -->

<!-- AI_BRIDGE_MANAGED:COORDINATED_VERSION_0_5_84:START -->

## Coordinated component version 0.5.85

Release date: 2026-07-15.

The active version is synchronized across:

- browser extension: `0.5.85`;
- local gateway and queue adapter: `0.5.85`;
- worker, runner, watcher, and diagnostics: `0.5.85`;
- Control Center launcher and inherited environment: `0.5.85`.

The Control Center launcher exports `AI_BRIDGE_VERSION` and
`AI_BRIDGE_CONTROL_CENTER_VERSION`, and displays the active version
in the console-window title.

Historical version references inside source comments are preserved.
Active declarations, protocol responses, assertions, and user-visible
version values are promoted.

Reload the extension and restart the running processes before runtime
health endpoints are expected to report `0.5.85`.

<!-- AI_BRIDGE_MANAGED:COORDINATED_VERSION_0_5_84:END -->

<!-- AI_BRIDGE_MANAGED:PLATFORM_ROUTING_AND_CAPABILITIES:END -->

<!-- AI_BRIDGE_MANAGED:GATEWAY_COMMAND_PLANE_0585:START -->

## Gateway command plane 0.5.85

The gateway now owns leases, retry, idempotency, payload references, results and capability dispatch. The compact API uses port `8767`.

See `docs/architecture/gateway-command-plane.md`.

<!-- AI_BRIDGE_MANAGED:GATEWAY_COMMAND_PLANE_0585:END -->

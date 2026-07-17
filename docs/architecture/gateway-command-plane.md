# Gateway command plane

Version: `0.5.85`

The existing gateway remains on port `8766`. A compact command API runs in the same gateway process on port `8767`.

Compact commands use additive `bridge2_*` SQLite tables, leases, expired-lease recovery, exponential retry with jitter, dead letters, persistent idempotency, SHA-256 payload references and stored result references.

The initial capability registry provides `runtime.health`, `queue.inspect`, `queue.dead_letters`, `git.inspect`, `file.read` and guarded `local.run`.

`local.run` requires `AI_BRIDGE_ENABLE_LOCAL_RUN=1`, `confirmed=true`, an allowlisted executable and a path allowed by `AI_BRIDGE_ALLOWED_ROOTS`.

The legacy transport and queue remain available during migration.

<!-- AI_BRIDGE_MANAGED:COMMAND_PLANE_DETAILS_0585:START -->

## Durable storage model

The additive command-plane schema includes:

- `bridge2_commands`;
- `bridge2_events`;
- `bridge2_payloads`;
- `bridge2_results`;
- lease, idempotency and dead-letter support.

The legacy `commands` table remains available during migration.

## Execution guarantees

The implementation provides:

- persistent command idempotency;
- finite leases;
- expired-lease recovery;
- bounded retry with exponential backoff and jitter;
- terminal dead-letter state;
- SHA-256 payload references;
- stored result references;
- capability registration and policy checks.

## Capability policy

The initial registry includes:

- `runtime.health`;
- `queue.inspect`;
- `queue.dead_letters`;
- `git.inspect`;
- `file.read`;
- guarded `local.run`.

`local.run` is disabled by default. Enabling it still requires confirmation,
an allowlisted executable and an allowed root.

## Coexistence

Port `8766` serves the legacy browser transport and diagnostics.

Port `8767` serves compact command-plane operations.

<!-- AI_BRIDGE_MANAGED:COMMAND_PLANE_DETAILS_0585:END -->

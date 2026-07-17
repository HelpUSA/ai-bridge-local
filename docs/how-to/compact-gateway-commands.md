# Compact gateway commands

Version: `0.5.85`

After applying this phase, restart gateway and worker, reload the unpacked extension and reload ChatGPT and HelpUS.

Validate with `python scripts/smoke/smoke_gateway_command_plane_0585.py`.

Queue administration:

- `python scripts/maintenance/queue_admin_0585.py summary`
- `python scripts/maintenance/queue_admin_0585.py requeue-expired`
- `python scripts/maintenance/queue_admin_0585.py dead-letters --limit 50`
- `python scripts/maintenance/queue_admin_0585.py retry COMMAND_ID`
- `python scripts/maintenance/queue_admin_0585.py cancel COMMAND_ID`

Large content must be stored with `POST http://127.0.0.1:8767/v1/payloads`; commands then carry only `payload_ref`.

<!-- AI_BRIDGE_MANAGED:COMPACT_COMMAND_OPERATIONS_0585:START -->

## Operational preflight

1. Confirm legacy gateway health on `127.0.0.1:8766`.
2. Confirm command-plane health on `127.0.0.1:8767`.
3. Confirm exactly one gateway and one worker.
4. Confirm no unexpected queued or delivering work.
5. Keep `local.run` disabled unless explicitly required.

Command identifiers are persistent idempotency keys.

Do not replay archived, failed or cancelled legacy commands without explicit
operator authorization.

## Validation commands

- `python scripts/smoke/smoke_gateway_command_plane_0585.py`
- `python -m pytest tests/test_gateway_command_plane_0585.py`
- `python scripts/maintenance/queue_admin_0585.py summary`

<!-- AI_BRIDGE_MANAGED:COMPACT_COMMAND_OPERATIONS_0585:END -->

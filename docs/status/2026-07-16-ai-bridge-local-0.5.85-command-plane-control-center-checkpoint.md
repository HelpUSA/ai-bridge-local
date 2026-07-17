# AI Bridge Local 0.5.85 - command plane and Control Center checkpoint

Date: 2026-07-16

## Result

The gateway-first command plane and Control Center recovery work are complete
in the current working tree.

## Implemented

- legacy gateway and diagnostics on port `8766`;
- compact command plane on port `8767`;
- additive `bridge2_*` persistence;
- leases, retries, dead letters and persistent idempotency;
- `local.run` disabled by default;
- Control Center gateway and worker autostart;
- Windows single-instance mutex;
- smart UI recovery through `controlcenter_launcher.ps1`;
- gateway and worker preserved during UI replacement;
- blocking refresh work moved outside the Tk thread;
- active queue separated from historical outcomes;
- read-only fallback for the historical `acked` total.

## Queue checkpoint

- active queued commands: `0`;
- active delivering commands: `0`;
- historical acked commands: `13827`;
- historical failed commands: `2912`;
- historical dead letters: `2418`.

Nine stale legacy queued commands were archived without deletion or replay.

## Launcher decision

`app_windows/controlcenter.bat` and
`app_windows/controlcenter_launcher.ps1` are official paired artifacts and must
be tracked together.

## Next activity

Resume M10:

1. add Control Center and launcher regression tests;
2. add an isolated HTTP E2E harness for ports `8766` and `8767`;
3. validate persistence, targets, idempotency, leases, retries and dead letters;
4. run browser interchat and read-only local-capability checks.

No commit or push was performed.

<!-- AI_BRIDGE_MANAGED:M10_VALIDATION_CHECKPOINT_0585:START -->

## M10 final integrated validation result

Result: `READY`.

Evidence:

- combined pytest: 15 passed;
- isolated HTTP E2E: passed;
- live interchat probe: `acked`;
- live read-only run-command probe: `acked`;
- run-command return code: `0`;
- gateway diagnostics smoke: passed;
- launcher validation: passed;
- runtime process counts remained one gateway, one worker and one Control
  Center;
- active queues returned to zero;
- probe database records were removed;
- `git diff --check`: passed;
- HEAD and `origin/main`: unchanged.

The interchat token remains visible in the destination chat. The database
backup is:

`backups/queue_local/queue_local_before_phase_023c4_m10b_20260717_133140_ab748ed4.db`

No commit or push was executed.

<!-- AI_BRIDGE_MANAGED:M10_VALIDATION_CHECKPOINT_0585:END -->

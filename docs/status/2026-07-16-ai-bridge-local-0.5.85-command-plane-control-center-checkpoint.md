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

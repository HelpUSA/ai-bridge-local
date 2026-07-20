# AI Bridge Local 0.5.86 ? M11 target isolation checkpoint

Date: `2026-07-18`

Baseline parent: `5abaca48317444fadad3e2497707527433363cb5`

Release: `0.5.86`

Live acceptance time: `2026-07-18T23:10:20.069551+00:00`

Confirmed target: `6a563525-4740-83e9-a8a1-212c8e5baf1e`

Live command: `m11_fixed_target_primary_20260718_225107_0bb256ee`

Observed acceptance:

- gateway-first selected `local_gateway`;
- original, routed and persisted target IDs matched;
- delivery used `button_click_confirmed`;
- delivery completed in one wrapper attempt;
- automatic target discovery was disabled;
- historical command and dead-letter fallback were disabled;
- one visible delivery was executed;
- probe database records were removed;
- the live acceptance suite passed 32 tests;
- release validation adds one explicit version test, bringing the suite to 33 tests.

## Release changes

- manifest name and version incremented to `0.5.86`;
- active runtime version literals incremented to `0.5.86`;
- historical document paths containing `0.5.85` preserved;
- browser heartbeat markers versioned for `0586`;
- target registry markers versioned for `0586`;
- registry smoke and contract test renamed to `0586`;
- exact browser target validation runs before injection;
- missing and ambiguous targets are blocked.

## Runtime boundary

The unpacked extension and all three local runtime processes must be reloaded after this commit. Runtime-facing version smokes are executed only after that restart.

## Next activity

M11 runtime reload verification, followed by M12.

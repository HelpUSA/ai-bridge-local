---
type: reference
status: draft
tags:
 - recipes
 - productivity
---

# Command recipes

Recipes are approved local workflows that reduce chat verbosity and make execution safer.

## MVP recipes

- safe_status: git status, recent log and selected markers.
- git_clean_guard: verify clean or allowlisted working tree.
- safe_patch: apply an exact patch to explicit files.
- safe_patch_test: patch plus validation.
- safe_patch_test_commit: patch, validate and commit exact files.
- inspect_failure: classify recent failure and suggest next action.
- recover_stale_worker: conservative stale PID recovery and worker restart.
- inspect_logs: return summarized recent logs and local log paths.

## Recipe contract

Each recipe declares:

- name
- purpose
- risk_level
- allowed cwd policy
- required inputs
- generated artifacts
- validation steps
- rollback behavior
- summary fields
- maximum chat output size

## Risk levels

- read
- write
- destructive
- network
- secret

Write recipes require repo and file allowlists. Destructive recipes require human confirmation.

## Output rule

Recipes return a concise summary by default. Full stdout and stderr stay local and are referenced by run_id or log path.

# AI Bridge Local - Operations Runbook

## Safe workflow

1. Start with `git status -sb`.
2. Confirm VERSION and current top commit.
3. Apply one small patch at a time.
4. Prefer docs-only changes for docs tasks.
5. Run required smokes.
6. Run `git diff --check`.
7. Show STATUS, DIFF_STAT, DOCS_CHANGED, validations, and changed files.
8. Stop for fiscalization before commit.

## Required validations for docs changes

```bash
python scripts/watcher/smoke_docs.py
python scripts/watcher/smoke_version_alignment.py
git diff --check
```

## Approval gates

Do not run cleanup, reset, commit, tag, push, or deploy without explicit approval. Do not change extension, gateway_local.py, brain_worker.py, or other code during docs-only tasks.

## Extension note

After any approved extension change, reload the Chrome extension and refresh the target chat tabs before a real delivery smoke.

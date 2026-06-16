# AI Bridge Local - Releases

## 0.5.11 - v0.5.11-composer-submit-guard

- Commit: c9ec07b
- Summary: guards composer submit against blocking modals and wrong submit buttons.
- Operational effect: reduces false positive delivery confirmation when the composer still contains text.

## 0.5.10 - v0.5.10-final-result-failure-continues

- Summary: keeps chat_can_continue=1 after failed final results.
- Operational effect: final failures can be analyzed and corrected without stopping the chat flow.

## 0.5.9 - v0.5.9-remove-accepted-running-notice

- Summary: removes accepted/running notice from the worker.
- Operational effect: expected flow is gateway queued feedback plus final AI_LOCAL_RUN.

## 0.5.8 - single worker guard

- Summary: adds a PID lock to prevent multiple brain_worker.py instances.
- Operational effect: reduces duplicate processing risk from concurrent workers.

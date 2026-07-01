from pathlib import Path

worker = Path("brain_worker.py").read_text(encoding="utf-8", errors="replace")
doc = Path("docs/COMMAND_ACCEPTED_PROGRESS_NOTICE.md").read_text(encoding="utf-8")
report = Path("reports/AI_BRIDGE_LOCAL_COMMAND_ACCEPTED_PROGRESS_NOTICE_2026-06-14.md").read_text(encoding="utf-8")

assert "[AI_LOCAL_RUN]" in worker
assert "Commands do not need to be split into smaller commands." in doc
assert "final [AI_LOCAL_RUN] result remains the authoritative execution result" in doc
assert "Kept final [AI_LOCAL_RUN] result unchanged." in report
assert "queued gateway feedback is informational" in report
assert "comando aceito, execucao iniciada" not in worker

print("OK command_accepted_progress_notice_smoke")

from pathlib import Path

worker = Path("brain_worker.py").read_text(encoding="utf-8")
doc = Path("docs/COMMAND_ACCEPTED_PROGRESS_NOTICE.md").read_text(encoding="utf-8")
report = Path("reports/AI_BRIDGE_LOCAL_COMMAND_ACCEPTED_PROGRESS_NOTICE_2026-06-14.md").read_text(encoding="utf-8")

assert 'def format_accepted_message(action):' in worker
assert 'def enqueue_accepted_message(action):' in worker
assert 'comando aceito, execucao iniciada' in worker
assert 'accepted_to_' in worker
assert 'status=running' in worker
assert 'no_reply=1' in worker
assert 'enqueue_accepted_message(action)\n:   invalid' not in worker
assert 'enqueue_accepted_message(action)\n        result = execute_command(payload, command_id)' in worker
assert '[AI_LOCAL_RUN]' in worker
assert 'Commands do not need to be split into smaller commands.' in doc
assert 'Kept final [AI_LOCAL_RUN] result unchanged.' in report

print("OK command_accepted_progress_notice_smoke")

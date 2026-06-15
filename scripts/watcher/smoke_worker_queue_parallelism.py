from pathlib import Path

worker = Path("brain_worker.py").read_text(encoding="utf-8")
doc = Path("docs/WORKER_QUEUE_PARALLELISM.md").read_text(encoding="utf-8")
report = Path("reports/AI_BRIDGE_LOCAL_WORKER_QUEUE_PARALLELISM_2026-06-15.md").read_text(encoding="utf-8")

assert "ThreadPoolExecutor" in worker
assert "MAX_PARALLEL_RUN_COMMANDS" in worker
assert "RUN_FUTURES" in worker
assert "CWD_LOCKS" in worker
assert "normalize_cwd_for_lock" in worker
assert "get_cwd_lock" in worker
assert "reap_run_futures" in worker
assert "submit_run_action" in worker
assert "def run_action(action):" in worker
assert "with cwd_lock:" in worker
assert "submit_run_action(action)" in worker
assert "enqueue_accepted_message(action)" in worker
assert "execute_command(payload, command_id)" in worker
assert "ThreadPoolExecutor" in doc
assert "cwd lock" in doc
assert "default max parallel run-command limit of three" in report

print("OK worker_queue_parallelism_smoke")

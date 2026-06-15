
from pathlib import Path

text = Path("brain_worker.py").read_text(encoding="utf-8")

required = [
    "WORKER_LOCK_PATH",
    "brain_worker.pid",
    "def acquire_single_worker_lock()",
    "def _pid_is_running",
    "def _release_single_worker_lock",
    "atexit.register",
    "another brain_worker.py is already running",
    "acquire_single_worker_lock()",
]

for marker in required:
    assert marker in text, marker

assert text.count("def acquire_single_worker_lock()") == 1
assert text.count("another brain_worker.py is already running") == 1

print("OK single_worker_guard_smoke")

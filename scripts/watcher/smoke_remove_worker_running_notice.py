
from pathlib import Path

worker = Path("brain_worker.py").read_text(encoding="utf-8")
for forbidden in [
    "comando aceito, execucao iniciada",
    "comando em execucao silenciosa",
    "worker_running_notice_disabled",
]:
    assert forbidden not in worker or ("running notice removed" in worker and worker.count(forbidden) == worker.count("# running notice removed"))

print("OK remove_worker_running_notice_smoke")

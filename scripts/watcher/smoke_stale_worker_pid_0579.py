# -*- coding: utf-8 -*-
from pathlib import Path
import os
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import brain_worker


def main():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        brain_worker.WORKER_LOCK_PATH = root / "brain_worker.pid"
        brain_worker.WORKER_ATTENTION_PATH = root / "brain_worker.needs_supervisor"
        brain_worker._pid_is_running = lambda pid: False
        brain_worker.WORKER_LOCK_PATH.write_text("99999999", encoding="utf-8")
        brain_worker.acquire_single_worker_lock()
        current = brain_worker.WORKER_LOCK_PATH.read_text(encoding="utf-8").strip()
        backups = list(root.glob("brain_worker.pid.stale_backup_*"))
        assert current == str(os.getpid()), current
        assert len(backups) == 1, backups
        assert backups[0].read_text(encoding="utf-8").strip() == "99999999"
        assert not brain_worker.WORKER_ATTENTION_PATH.exists()
        brain_worker._release_single_worker_lock()
        assert not brain_worker.WORKER_LOCK_PATH.exists()
    print("SMOKE_STALE_WORKER_PID_0579_OK")


if __name__ == "__main__":
    main()

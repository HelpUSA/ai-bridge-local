# -*- coding: utf-8 -*-
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import brain_worker


def main():
    calls = {}

    def fake_get_json(url, timeout=10):
        calls.setdefault("get_json", []).append(url)
        return {
            "ok": True,
            "action": {
                "command_id": "smoke-0581",
                "action": "run-command",
                "payload": {"command": ["python", "-c", "print('ok')"]},
            },
        }

    def fake_submit_run_action(action):
        calls.setdefault("submit", []).append(action)
        return True

    def fake_execute_command(payload, command_id="unknown"):
        calls.setdefault("execute_inline", []).append(command_id)
        return {"return_code": 0, "stdout": "should not run", "stderr": ""}

    orig_get_json = brain_worker.get_json
    orig_submit = brain_worker.submit_run_action
    orig_exec = brain_worker.execute_command
    try:
        brain_worker.get_json = fake_get_json
        brain_worker.submit_run_action = fake_submit_run_action
        brain_worker.execute_command = fake_execute_command
        brain_worker.poll_source("src-0581")
    finally:
        brain_worker.get_json = orig_get_json
        brain_worker.submit_run_action = orig_submit
        brain_worker.execute_command = orig_exec

    assert calls["submit"][0]["command_id"] == "smoke-0581"
    assert "execute_inline" not in calls

    orig_qa_adapter = brain_worker.queue_adapter
    try:
        brain_worker.queue_adapter = None
        assert brain_worker.worker_heartbeat() is False
    finally:
        brain_worker.queue_adapter = orig_qa_adapter

    print("SMOKE_0581_WORKER_SUPERVISOR_OK")


if __name__ == "__main__":
    main()

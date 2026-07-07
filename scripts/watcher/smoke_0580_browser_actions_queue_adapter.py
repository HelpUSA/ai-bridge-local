# -*- coding: utf-8 -*-
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import gateway_local
import queue_adapter


def main():
    with tempfile.TemporaryDirectory() as td:
        db = os.path.join(td, "q.db")
        gateway_local.DB_PATH = db
        gateway_local.init_db()

        ev = gateway_local.record_browser_event({
            "event_id": "ev-0580",
            "event_type": "browser.chat_snapshot",
            "chat_id": "chat-1",
            "payload": {"ok": True},
        })
        assert ev["ok"] is True
        assert ev["inserted"] is True

        duplicate = gateway_local.record_browser_event({
            "event_id": "ev-0580",
            "event_type": "browser.chat_snapshot",
        })
        assert duplicate["inserted"] is False

        act = gateway_local.create_browser_action({
            "action_id": "act-0580",
            "action_type": "browser.inject_message",
            "chat_id": "chat-1",
            "payload": {"message": "ok"},
        })
        assert act["ok"] is True

        claimed = gateway_local.claim_browser_action("chat-1")
        assert claimed["action_id"] == "act-0580"
        assert claimed["status"] == "delivered_to_extension"

        result = gateway_local.record_browser_action_result({
            "action_id": "act-0580",
            "status": "sent_to_chat",
            "result": {"ok": True},
        })
        assert result["status"] == "sent_to_chat"

        status = gateway_local.fetch_control_status()
        assert status["browser_events_total"] == 1
        assert status["browser_action_status"]["sent_to_chat"] == 1

        adapter = queue_adapter.QueueAdapter(db)
        enqued = adapter.enqueue({
            "command_id": "cmd-0580",
            "source_chat_id": "src",
            "target_chat_id": "tgt",
            "action": "run-command",
            "delivery_kind": "local_capability",
            "payload": {"cmd": "ok"},
        })
        assert enqued["ok"] is True

        command = adapter.claim("tgt", "src")
        assert command["command_id"] == "cmd-0580"
        assert command["payload"]["cmd"] == "ok"
        assert adapter.ack("cmd-0580", return_code=0, stdout="ok") is True
        assert adapter.heartbeat("worker-0580")["ok"] is True

    print("SMOKE_0580_BROWSER_ACTIONS_QUEUE_ADAPTER_OK")


if __name__ == "__main__":
    main()

from __future__ import annotations

import importlib.util
import json
import os
import sqlite3
import sys
import threading
import uuid
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@contextmanager
def loaded_module(
    path: Path,
    prefix: str,
    environment: dict[str, str] | None = None,
):
    previous = {}

    for key, value in (environment or {}).items():
        previous[key] = os.environ.get(key)
        os.environ[key] = value

    name = prefix + "_" + uuid.uuid4().hex
    spec = importlib.util.spec_from_file_location(name, path)

    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module

    try:
        spec.loader.exec_module(module)
        yield module

    finally:
        sys.modules.pop(name, None)

        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


@contextmanager
def running_server(server):
    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )

    thread.start()

    try:
        host, port = server.server_address[:2]
        yield f"http://{host}:{port}"

    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

        assert not thread.is_alive()


def request_json(
    base: str,
    path: str,
    method: str = "GET",
    body: dict | None = None,
) -> tuple[int, dict]:
    raw = None

    if body is not None:
        raw = json.dumps(
            body,
            ensure_ascii=False,
        ).encode("utf-8")

    request = Request(
        base + path,
        data=raw,
        method=method,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urlopen(request, timeout=5) as response:
            return (
                response.status,
                json.loads(
                    response.read().decode("utf-8")
                ),
            )

    except HTTPError as error:
        payload = error.read()

        return (
            error.code,
            json.loads(payload.decode("utf-8"))
            if payload
            else {},
        )


def test_legacy_gateway_http_e2e() -> None:
    gateway_path = ROOT / "gateway_local.py"

    with TemporaryDirectory() as temporary:
        database = Path(temporary) / "legacy.db"

        with loaded_module(
            gateway_path,
            "legacy_gateway_http_e2e",
        ) as module:
            module.DB_PATH = str(database)
            module.init_db()

            server = module.ThreadingHTTPServer(
                ("127.0.0.1", 0),
                module.GatewayHandler,
            )

            with running_server(server) as base:
                status, health = request_json(
                    base,
                    "/health",
                )

                assert status == 200
                assert health["ok"] is True
                assert health["service"] == "ai-bridge-local"

                send_id = "legacy-send-http-e2e-0585"

                send_envelope = {
                    "schema": "ai_bridge_local.envelope",
                    "schema_version": 1,
                    "version": "1",
                    "command_id": send_id,
                    "action": "send-chat-message",
                    "type": "send-chat-message",
                    "source_chat_id": "e2e-source",
                    "target_chat_id": "e2e-target",
                    "delivery_kind": "inter_agent_message",
                    "conversation_id": "e2e-conversation",
                    "from_agent": "pytest",
                    "force_gateway": True,
                    "no_reply": True,
                    "message": "LEGACY_SEND_HTTP_E2E_OK",
                    "payload": {
                        "message": "LEGACY_SEND_HTTP_E2E_OK",
                    },
                }

                status, queued_send = request_json(
                    base,
                    "/bridge/commands",
                    method="POST",
                    body=send_envelope,
                )

                assert status == 200, queued_send
                assert queued_send["ok"] is True
                assert queued_send["status"] == "queued"

                status, duplicate = request_json(
                    base,
                    "/bridge/commands",
                    method="POST",
                    body=send_envelope,
                )

                assert status == 409, duplicate
                assert duplicate["error"] == "duplicate"

                run_id = "legacy-run-http-e2e-0585"

                run_envelope = {
                    "schema": "ai_bridge_local.envelope",
                    "schema_version": 1,
                    "version": "1",
                    "command_id": run_id,
                    "action": "run-command",
                    "type": "run-command",
                    "source_chat_id": "e2e-source",
                    "target_chat_id": "gateway-brain-supervisor",
                    "delivery_kind": "local_capability",
                    "conversation_id": "e2e-conversation",
                    "from_agent": "pytest",
                    "force_gateway": True,
                    "no_reply": False,
                    "payload": {
                        "command": [
                            "python",
                            "-X",
                            "utf8",
                            "-c",
                            "print('LEGACY_RUN_HTTP_E2E_OK')",
                        ],
                        "cwd": temporary,
                        "timeout_seconds": 5,
                    },
                }

                status, queued_run = request_json(
                    base,
                    "/bridge/commands",
                    method="POST",
                    body=run_envelope,
                )

                assert status == 200, queued_run
                assert queued_run["ok"] is True
                assert queued_run["status"] == "queued"

                query = urlencode(
                    {
                        "chat_id": queued_run["target_chat_id"],
                        "source_chat_id": "e2e-source",
                    }
                )

                status, delivery = request_json(
                    base,
                    "/bridge/next-action?" + query,
                )

                assert status == 200, delivery
                assert delivery["ok"] is True
                assert delivery["action"] is not None
                assert delivery["action"]["command_id"] == run_id
                assert delivery["action"]["action"] == "run-command"

                status, acknowledged = request_json(
                    base,
                    "/bridge/acks",
                    method="POST",
                    body={
                        "command_id": run_id,
                        "status": "acked",
                        "return_code": 0,
                        "stdout": "LEGACY_RUN_HTTP_E2E_OK",
                        "stderr": "",
                    },
                )

                assert status == 200
                assert acknowledged["ok"] is True

            connection = sqlite3.connect(database)

            try:
                send_row = connection.execute(
                    """
                    SELECT status
                    FROM commands
                    WHERE command_id = ?
                    """,
                    (send_id,),
                ).fetchone()

                run_row = connection.execute(
                    """
                    SELECT status, return_code, stdout
                    FROM commands
                    WHERE command_id = ?
                    """,
                    (run_id,),
                ).fetchone()

            finally:
                connection.close()

            assert send_row == ("queued",)

            assert run_row == (
                "acked",
                0,
                "LEGACY_RUN_HTTP_E2E_OK",
            )


def test_command_plane_http_e2e() -> None:
    command_path = ROOT / "gateway_command_plane.py"

    with TemporaryDirectory() as temporary:
        database = Path(temporary) / "command-plane.db"

        environment = {
            "AI_BRIDGE_QUEUE_DB": str(database),
            "AI_BRIDGE_COMMAND_HOST": "127.0.0.1",
            "AI_BRIDGE_COMMAND_PORT": "0",
            "AI_BRIDGE_COMMAND_HTTP_LOG": "0",
            "AI_BRIDGE_ENABLE_LOCAL_RUN": "0",
        }

        with loaded_module(
            command_path,
            "command_plane_http_e2e",
            environment,
        ) as module:
            server = module.ThreadingHTTPServer(
                ("127.0.0.1", 0),
                module.Handler,
            )

            with running_server(server) as base:
                status, health = request_json(
                    base,
                    "/health",
                )

                assert status == 200
                assert health["ok"] is True

                assert (
                    health["service"]
                    == "ai-bridge-command-plane"
                )

                status, capabilities = request_json(
                    base,
                    "/v1/capabilities",
                )

                assert status == 200
                assert capabilities["ok"] is True

                names = {
                    item["name"]
                    for item in capabilities["capabilities"]
                }

                assert {
                    "runtime.health",
                    "queue.inspect",
                    "local.run",
                } <= names

                status, payload = request_json(
                    base,
                    "/v1/payloads",
                    method="POST",
                    body={
                        "content": "COMMAND_PLANE_HTTP_E2E_OK",
                        "encoding": "utf-8",
                        "ttl_seconds": 60,
                    },
                )

                assert status == 201, payload
                assert payload["ok"] is True

                status, summary = request_json(
                    base,
                    "/v1/queue/summary",
                )

                assert status == 200
                assert summary["ok"] is True
                assert isinstance(summary["queue"], dict)

                status, requeue = request_json(
                    base,
                    "/v1/admin/requeue-expired",
                    method="POST",
                    body={},
                )

                assert status == 200
                assert requeue["ok"] is True

                status, missing = request_json(
                    base,
                    "/v1/commands/does-not-exist",
                )

                assert status == 404
                assert missing["ok"] is False

        assert database.is_file()

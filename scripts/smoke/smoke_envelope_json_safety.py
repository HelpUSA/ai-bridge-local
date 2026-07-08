#!/usr/bin/env python3
"""Smoke tests for JSON-safe envelope tooling.

Covers the 0.5.84 docs+tooling failure classes:
raw Windows backslashes and invalid physical multiline JSON bodies.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WATCHER = ROOT / "scripts" / "watcher"
sys.path.insert(0, str(WATCHER))

from envelope_json_safe_helper import (  # noqa: E402
    END_MARKER,
    START_MARKER,
    EnvelopeSafetyError,
    build_run_command,
    build_send_chat_message,
    render_envelope,
    validate_envelope_text,
)


def body(marked: str) -> str:
    lines = marked.strip().splitlines()
    assert lines[0] == START_MARKER
    assert lines[-1] == END_MARKER
    return "\n".join(lines[1:-1])


def assert_rejects(raw: str) -> None:
    try:
        validate_envelope_text(raw)
    except EnvelopeSafetyError:
        return
    raise AssertionError("expected envelope to be rejected")


def main() -> int:
    print("SMOKE_ENVELOPE_JSON_SAFETY_START", flush=True)

    win_path = "C:" + chr(92) + "Temp" + chr(92) + "ai-bridge" + chr(92) + "out.txt"
    run_env = build_run_command(
        source_chat_id="source-chat",
        command_id="smoke_json_safe_run",
        cwd="D:/dev/autocode/ai-bridge-local",
        command=["python", "-c", "print(" + repr(win_path) + ")"],
        timeout_seconds=30,
    )
    marked = render_envelope(run_env)
    run_body = body(marked)
    assert "\n" not in run_body
    assert chr(92) + chr(92) in run_body, "Windows backslashes must be escaped"
    assert "out.txt" in json.loads(run_body)["payload"]["command"][-1]

    message = "line one" + chr(10) + "line two"
    msg_env = build_send_chat_message(
        source_chat_id="source-chat",
        target_chat_id="target-chat",
        command_id="smoke_json_safe_message",
        message=message,
        force_gateway=True,
    )
    msg_body = body(render_envelope(msg_env))
    assert "\n" not in msg_body
    assert json.loads(msg_body)["message"] == message

    raw_backslash_bad = (
        START_MARKER
        + chr(10)
        + '{"schema":"ai_bridge_local.envelope","schema_version":1,"command_id":"bad","source_chat_id":"s","target_chat_id":"t","action":"send-chat-message","delivery_kind":"inter_agent_message","message":"C:'
        + chr(92)
        + 'dev'
        + chr(92)
        + 'bad"}'
        + chr(10)
        + END_MARKER
    )
    assert_rejects(raw_backslash_bad)

    raw_multiline_bad = (
        START_MARKER
        + chr(10)
        + '{"schema":"ai_bridge_local.envelope","schema_version":1,"command_id":"bad2","source_chat_id":"s","target_chat_id":"t","action":"send-chat-message","delivery_kind":"inter_agent_message","message":"line1'
        + chr(10)
        + 'line2"}'
        + chr(10)
        + END_MARKER
    )
    assert_rejects(raw_multiline_bad)

    print("SMOKE_ENVELOPE_JSON_SAFETY_OK", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

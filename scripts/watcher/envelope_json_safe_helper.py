#!/usr/bin/env python3
"""JSON-safe AI Bridge Local envelope helper.

Tooling-only helper: it renders strict JSON envelopes without changing gateway,
protocol, queue, or browser delivery behavior.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

START_MARKER = "@@AI_BRIDGE_LOCAL_START@@"
END_MARKER = "@@AI_BRIDGE_LOCAL_END@@"
SCHEMA = "ai_bridge_local.envelope"
REQUIRED_KEYS = (
    "schema",
    "schema_version",
    "command_id",
    "source_chat_id",
    "target_chat_id",
    "action",
    "delivery_kind",
)


class EnvelopeSafetyError(ValueError):
    """Raised when text is not safe strict JSON envelope content."""



def _json_body_from_text(raw: str) -> str:
    text = raw.strip()
    lines = text.splitlines()
    if lines and lines[0].strip() == START_MARKER:
        if not lines or lines[-1].strip() != END_MARKER:
            raise EnvelopeSafetyError("missing end marker")
        return "\n".join(lines[1:-1]).strip()
    return text


def validate_envelope_text(raw: str) -> dict[str, Any]:
    """Parse and validate marked or unmarked envelope text."""
    body = _json_body_from_text(raw)
    if "\n" in body or "\r" in body:
        raise EnvelopeSafetyError("JSON body must be one physical line")
    try:
        env = json.loads(body)
    except json.JSONDecodeError as exc:
        raise EnvelopeSafetyError(f"invalid strict JSON: {exc}") from exc

    if not isinstance(env, dict):
        raise EnvelopeSafetyError("envelope must be a JSON object")

    missing = [key for key in REQUIRED_KEYS if key not in env]
    if missing:
        raise EnvelopeSafetyError("missing required keys: " + ",".join(missing))
    if env["schema"] != SCHEMA:
        raise EnvelopeSafetyError("invalid schema")

    action = env["action"]
    delivery_kind = env["delivery_kind"]
    if action == "send-chat-message":
        if delivery_kind != "inter_agent_message":
            raise EnvelopeSafetyError("send-chat-message requires inter_agent_message")
        if not isinstance(env.get("message"), str):
            raise EnvelopeSafetyError("send-chat-message requires string message")
    elif action == "run-command":
        if delivery_kind != "local_capability":
            raise EnvelopeSafetyError("run-command requires local_capability")
        if env.get("target_chat_id") != "gateway-brain-supervisor":
            raise EnvelopeSafetyError("run-command target must be gateway-brain-supervisor")
        payload = env.get("payload")
        if not isinstance(payload, dict):
            raise EnvelopeSafetyError("run-command requires payload object")
        command = payload.get("command")
        if not isinstance(command, list) or not all(isinstance(part, str) for part in command):
            raise EnvelopeSafetyError("payload.command must be a list of strings")
    else:
        raise EnvelopeSafetyError("unsupported action: " + str(action))

    return env


def render_envelope(env: dict[str, Any]) -> str:
    """Render an envelope with strict JSON between bridge markers."""
    body = json.dumps(env, ensure_ascii=False, separators=(",", ":"))
    if "\n" in body or "\r" in body:
        raise EnvelopeSafetyError("json.dumps produced unexpected physical newline")
    validate_envelope_text(body)
    return START_MARKER + "\n" + body + "\n" + END_MARKER + "\n"


def build_run_command(
    *,
    source_chat_id: str,
    command_id: str,
    cwd: str,
    command: list[str],
    timeout_seconds: int = 120,
    conversation_id: str = "ai_bridge_local_json_safe_helper",
    from_agent: str = "envelope_json_safe_helper",
) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "schema_version": 1,
        "command_id": command_id,
        "action": "run-command",
        "source_chat_id": source_chat_id,
        "target_chat_id": "gateway-brain-supervisor",
        "delivery_kind": "local_capability",
        "conversation_id": conversation_id,
        "from_agent": from_agent,
        "payload": {
            "cwd": cwd,
            "timeout_seconds": timeout_seconds,
            "command": command or ["git", "status", "--short"],
        },
    }


def build_send_chat_message(
    *,
    source_chat_id: str,
    target_chat_id: str,
    command_id: str,
    message: str,
    conversation_id: str = "ai_bridge_local_json_safe_helper",
    from_agent: str = "envelope_json_safe_helper",
    force_gateway: bool = False,
) -> dict[str, Any]:
    env: dict[str, Any] = {
        "schema": SCHEMA,
        "schema_version": 1,
        "command_id": command_id,
        "action": "send-chat-message",
        "source_chat_id": source_chat_id,
        "target_chat_id": target_chat_id,
        "delivery_kind": "inter_agent_message",
        "conversation_id": conversation_id,
        "from_agent": from_agent,
        "message": message,
    }
    if force_gateway:
        env["force_gateway"] = True
    return env


def build_from_args(argv: list[str] | None = None) -> str:
    parser = argparse.ArgumentParser(description="Build strict JSON AI Bridge Local envelopes.")
    parser.add_argument("--source", required=True, help="source_chat_id")
    parser.add_argument("--target", required=True, help="target_chat_id or gateway-brain-supervisor")
    parser.add_argument("--action", required=True, choices=("send-chat-message", "run-command"))
    parser.add_argument("--id", required=True, help="command_id")
    parser.add_argument("--conversation-id", default="ai_bridge_local_json_safe_helper")
    parser.add_argument("--from-agent", default="envelope_json_safe_helper")
    parser.add_argument("--message", default="")
    parser.add_argument("--force-gateway", action="store_true")
    parser.add_argument("--cwd", default="D:/dev/autocode/ai-bridge-local")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--command", nargs=argparse.REMAINDER)
    parser.add_argument("--output-file", default="")
    args = parser.parse_args(argv)

    if args.action == "send-chat-message":
        if not args.message:
            raise SystemExit("--message is required for send-chat-message")
        env = build_send_chat_message(
            source_chat_id=args.source,
            target_chat_id=args.target,
            command_id=args.id,
            message=args.message,
            conversation_id=args.conversation_id,
            from_agent=args.from_agent,
            force_gateway=args.force_gateway,
        )
    else:
        if args.target != "gateway-brain-supervisor":
            raise SystemExit("run-command target must be gateway-brain-supervisor")
        env = build_run_command(
            source_chat_id=args.source,
            command_id=args.id,
            cwd=args.cwd,
            command=args.command or ["git", "status", "--short"],
            timeout_seconds=args.timeout,
            conversation_id=args.conversation_id,
            from_agent=args.from_agent,
        )

    rendered = render_envelope(env)
    if args.output_file:
        output = Path(args.output_file)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    return rendered


def main() -> int:
    print(build_from_args(), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

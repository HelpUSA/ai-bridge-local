from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKGROUND = ROOT / "extension" / "background.js"
CONTENT = ROOT / "extension" / "content_script.js"

START_MARKER = "@@" + "AI_BRIDGE_LOCAL_START" + "@@"
END_MARKER = "@@" + "AI_BRIDGE_LOCAL_END" + "@@"


def parse_block(text: str) -> dict:
    stripped = text.strip()
    if stripped.count(START_MARKER) != 1 or stripped.count(END_MARKER) != 1:
        raise ValueError("multiple_or_missing_blocks")
    start = stripped.index(START_MARKER)
    end = stripped.index(END_MARKER)
    if end <= start:
        raise ValueError("invalid_marker_order")
    if stripped[:start].strip() or stripped[end + len(END_MARKER) :].strip():
        raise ValueError("text_outside_block")
    body = stripped[start + len(START_MARKER) : end].strip()
    if not body:
        raise ValueError("empty_json_body")
    data = json.loads(body)
    if not isinstance(data, dict):
        raise ValueError("json_not_object")
    if not str(data.get("command_id", "")).strip():
        raise ValueError("missing_command_id")
    return data


def captured_readonly_gate(envelope: dict) -> bool:
    payload = envelope.get("payload") if isinstance(envelope.get("payload"), dict) else {}
    parts = []
    if isinstance(payload.get("command"), list):
        parts.append(" ".join(map(str, payload["command"])))
    if payload.get("script_text"):
        parts.append(str(payload["script_text"]))
    if payload.get("cwd"):
        parts.append(str(payload["cwd"]))
    text = (" " + " ".join(parts) + " ").lower()
    blocked = [
        "remove-item",
        " set-content",
        " add-content",
        " out-file",
        " git add",
        " git commit",
        " git push",
        " npm install",
        " pip install",
        " invoke-expression",
        " iex",
        " curl",
        " del ",
        " erase ",
        " rm ",
        " rmdir ",
        " move ",
        " mv ",
        " copy ",
        " cp ",
    ]
    if any(token in text for token in blocked):
        return False
    return (
        "get-childitem" in text
        or " dir " in text
        or "git status" in text
        or "git diff --name-only" in text
        or "git diff --stat" in text
    )


def main() -> None:
    background = BACKGROUND.read_text(encoding="utf-8", errors="replace")
    content = CONTENT.read_text(encoding="utf-8", errors="replace")

    required_background = [
        "validateAiBridgeCapturedEnvelopeMessage",
        "AI_BRIDGE_CAPTURED_ENVELOPE",
        "run_command_rejected_by_readonly_gate",
        "send_chat_message_requires_inter_agent_message",
        "capturedEnvelope",
    ]
    required_content = [
        "installAiBridgeGeminiCapturedEnvelopeBridge",
        "parseCapturedEnvelopeText",
        "MutationObserver",
        "AI_BRIDGE_CAPTURED_ENVELOPE",
        "text_outside_block",
        "sessionStorage",
    ]

    missing = [item for item in required_background if item not in background]
    missing.extend(item for item in required_content if item not in content)
    if missing:
        raise AssertionError("missing expected markers: " + ", ".join(missing))

    valid = {
        "command_id": "smoke_valid",
        "action": "send-chat-message",
        "type": "send-chat-message",
        "delivery_kind": "inter_agent_message",
        "source_chat_id": "gemini-smoke",
        "target_chat_id": "chat-smoke",
        "conversation_id": "smoke",
        "message": "hello",
    }
    parsed = parse_block(f"{START_MARKER}\n{json.dumps(valid, separators=(',', ':'))}\n{END_MARKER}")
    assert parsed["command_id"] == "smoke_valid"

    cases = [
        ("extra\n" + START_MARKER + "\n{}\n" + END_MARKER, "text_outside_block"),
        (START_MARKER + "\n{}\n" + END_MARKER + "\n" + START_MARKER + "\n{}\n" + END_MARKER, "multiple_or_missing_blocks"),
        (START_MARKER + "\nnot-json\n" + END_MARKER, "Expecting value"),
        (START_MARKER + "\n{}\n" + END_MARKER, "missing_command_id"),
    ]
    for payload, expected in cases:
        try:
            parse_block(payload)
        except Exception as exc:
            if expected not in str(exc):
                raise AssertionError(f"expected {expected!r}, got {exc!r}") from exc
        else:
            raise AssertionError(f"case should fail: {expected}")

    readonly = {
        "command_id": "smoke_readonly",
        "action": "run-command",
        "delivery_kind": "local_capability",
        "payload": {"command": ["git", "status", "-sb"]},
    }
    destructive = {
        "command_id": "smoke_destructive",
        "action": "run-command",
        "delivery_kind": "local_capability",
        "payload": {"command": ["cmd", "/c", "git status && del important.txt"]},
    }
    assert captured_readonly_gate(readonly)
    assert not captured_readonly_gate(destructive)

    print("OK smoke_gemini_auto_envelope_roundtrip")


if __name__ == "__main__":
    main()

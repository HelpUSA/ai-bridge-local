# -*- coding: utf-8 -*-
"""AI Bridge Local - Brain Worker v0.1.2"""
import json
import os
import subprocess
from pathlib import Path
import time
import urllib.request

GATEWAY = "http://127.0.0.1:8766"
VERSION = "0.1.3"

def now_iso():
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()

def post_json(url, data, timeout=10):
    raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=raw, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())

def get_json(url, timeout=10):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read())

def truncate(value, limit=5000):
    value = str(value or "")
    if len(value) <= limit:
        return value
    return value[:limit] + "\n...[truncated]"

def normalize_command(cmd):
    if isinstance(cmd, list):
        return cmd
    if isinstance(cmd, str) and cmd.strip():
        if os.name == "nt":
            return ["cmd", "/c", cmd]
        return ["sh", "-lc", cmd]
    return []

def prepare_temp_script(payload, command_id):
    script_text = payload.get("script_text")
    if not isinstance(script_text, str) or not script_text:
        return None

    ext = str(payload.get("script_ext") or ".ps1").strip()
    if not ext.startswith("."):
        ext = "." + ext

    safe_id = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in str(command_id or "script"))[:80]
    scripts_dir = Path("temp") / "watcher_scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    script_path = scripts_dir / (safe_id + ext)
    script_path.write_text(script_text, encoding="utf-8")
    return str(script_path)


def execute_command(payload, command_id="unknown"):
    if not isinstance(payload, dict):
        return {"return_code": -1, "stdout": "", "stderr": "invalid_payload_not_object"}

    script_path = prepare_temp_script(payload, command_id)
    cmd = normalize_command(payload.get("command"))
    if script_path:
        if not cmd:
            if script_path.lower().endswith(".ps1"):
                cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script_path]
            elif script_path.lower().endswith(".py"):
                cmd = ["python", script_path]
            else:
                cmd = [script_path]
        else:
            cmd = [str(x).replace("{script_path}", script_path) for x in cmd]
    cwd = payload.get("cwd") or "."
    timeout = int(payload.get("timeout_seconds") or 30)

    if not cmd:
        return {"return_code": -1, "stdout": "", "stderr": "missing_payload_command"}

    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            shell=False
        )
        return {"return_code": result.returncode, "stdout": truncate(result.stdout), "stderr": truncate(result.stderr)}
    except subprocess.TimeoutExpired:
        return {"return_code": -1, "stdout": "", "stderr": "timeout"}
    except Exception as e:
        return {"return_code": -1, "stdout": "", "stderr": str(e)}

def format_result_message(action, result, status):
    command_id = action.get("command_id", "unknown")
    payload = action.get("payload", {}) if isinstance(action.get("payload", {}), dict) else {}
    cmd = payload.get("command", "")
    cwd = payload.get("cwd", ".")

    return (
        "[AI_LOCAL_RUN]\n"
        f"id={command_id}\n"
        f"status={status}\n"
        f"return_code={result.get('return_code')}\n"
        "no_reply=1\n"
        f"cwd={cwd}\n"
        f"command={json.dumps(cmd, ensure_ascii=False)}\n"
        "stdout=\n" + truncate(result.get("stdout", ""), 3500) + "\n"
        "stderr=\n" + truncate(result.get("stderr", ""), 1500)
    )

def enqueue_result_message(action, result, status):
    source_chat_id = action.get("source_chat_id", "")
    if not source_chat_id:
        return

    command_id = action.get("command_id", "unknown")
    result_command_id = "result_to_" + command_id

    body = {
        "schema": "ai_bridge_local.envelope",
        "schema_version": 1,
        "command_id": result_command_id,
        "action": "send-chat-message",
        "source_chat_id": "gateway-brain-supervisor",
        "target_chat_id": source_chat_id,
        "delivery_kind": "local_inter_agent_message",
        "conversation_id": (action.get("conversation_id") or "local_run_command") + "_result",
        "from_agent": "AI Bridge Local Worker " + VERSION,
        "message": format_result_message(action, result, status)
    }

    try:
        post_json(f"{GATEWAY}/bridge/commands", body)
        print(f"[worker] Result enqueued: {result_command_id}")
    except Exception as e:
        print(f"[worker] Result enqueue skipped/error: {e}")

def poll_source(source_chat_id):
    try:
        data = get_json(f"{GATEWAY}/bridge/next-action?chat_id=gateway-brain-supervisor&source_chat_id={source_chat_id}")
    except Exception as e:
        print(f"[worker] Poll error for source {source_chat_id}: {e}")
        return

    action = data.get("action") if data else None
    if not action:
        return

    command_id = action.get("command_id", "unknown")
    action_type = action.get("action", "")
    payload = action.get("payload", {})

    if action_type == "send-chat-message":
        print(f"[worker] Skip {command_id} (send-chat-message - extension handles)")
        return

    print(f"[worker] Running: {command_id} ({action_type}) source={source_chat_id}")

    if action_type == "run-command":
        result = execute_command(payload, command_id)
        status = "acked" if result["return_code"] == 0 else "failed"
        enqueue_result_message(action, result, status)
    else:
        result = {"return_code": 0, "stdout": f"OK {action_type}", "stderr": ""}
        status = "acked"

    ack = {
        "command_id": command_id,
        "status": status,
        "return_code": result["return_code"],
        "stdout": result.get("stdout", ""),
        "stderr": result.get("stderr", ""),
        "error": result.get("stderr", "") if status == "failed" else ""
    }

    try:
        post_json(f"{GATEWAY}/bridge/acks", ack)
        print(f"[worker] {command_id}: {status}")
    except Exception as e:
        print(f"[worker] ACK error: {e}")


def poll_once():
    try:
        data = get_json(f"{GATEWAY}/bridge/pending-sources?target_chat_id=gateway-brain-supervisor")
    except Exception as e:
        print(f"[worker] Pending sources error: {e}")
        return

    sources = data.get("sources", []) if data else []
    if not sources:
        return

    for source in sources:
        source_chat_id = source.get("source_chat_id", "") if isinstance(source, dict) else str(source)
        if source_chat_id:
            poll_source(source_chat_id)

def main():
    print(f"[worker] AI Bridge Local Worker v{VERSION} - Porta 8766")
    print("[worker] Ctrl+C to stop")
    while True:
        poll_once()
        time.sleep(2)

if __name__ == "__main__":
    main()

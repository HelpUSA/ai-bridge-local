# -*- coding: utf-8 -*-
"""AI Bridge Local - Brain Worker v0.1.2"""
import json
import os
import subprocess
from pathlib import Path
import time
import urllib.request
import threading
from concurrent.futures import ThreadPoolExecutor

GATEWAY = "http://127.0.0.1:8766"
VERSION = "0.1.5"

MAX_PARALLEL_RUN_COMMANDS = int(os.environ.get("AI_BRIDGE_MAX_PARALLEL_RUN_COMMANDS", "3"))
RUN_EXECUTOR = ThreadPoolExecutor(max_workers=MAX_PARALLEL_RUN_COMMANDS)
RUN_FUTURES = {}
RUN_FUTURES_LOCK = threading.Lock()
CWD_LOCKS = {}
CWD_LOCKS_LOCK = threading.Lock()


def normalize_cwd_for_lock(payload):
    if not isinstance(payload, dict):
        return "."
    cwd = str(payload.get("cwd") or ".").replace("\\", "/").rstrip("/")
    return cwd or "."


def get_cwd_lock(cwd):
    with CWD_LOCKS_LOCK:
        lock = CWD_LOCKS.get(cwd)
        if lock is None:
            lock = threading.Lock()
            CWD_LOCKS[cwd] = lock
        return lock


def reap_run_futures():
    done = []
    with RUN_FUTURES_LOCK:
        for future, command_id in list(RUN_FUTURES.items()):
            if future.done():
                done.append((future, command_id))
                RUN_FUTURES.pop(future, None)
    for future, command_id in done:
        try:
            future.result()
        except Exception as exc:
            print(f"[worker] Future error for {command_id}: {exc}")


def submit_run_action(action):
    command_id = action.get("command_id", "unknown")
    future = RUN_EXECUTOR.submit(run_action, action)
    with RUN_FUTURES_LOCK:
        RUN_FUTURES[future] = command_id
    print(f"[worker] Submitted parallel run: {command_id}")
    return True


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

    intent = payload.get("intent")
    if intent and not payload.get("command") and not payload.get("script_text") and not payload.get("script_path"):
        intent_command = [
            "python",
            "scripts/watcher/command_intake.py",
            "--intent",
            str(intent),
            "--command-id",
            str(command_id),
            "--cwd",
            str(payload.get("cwd") or "."),
        ]
        if payload.get("execute_intent"):
            intent_command.append("--execute")
        if payload.get("timeout_seconds"):
            intent_command.extend(["--timeout", str(int(payload.get("timeout_seconds")))])
        payload = dict(payload)
        payload["command"] = intent_command

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
            timeout=timeout,
        )
        return {"return_code": result.returncode, "stdout": truncate(result.stdout), "stderr": truncate(result.stderr)}
    except subprocess.TimeoutExpired:
        return {"return_code": -1, "stdout": "", "stderr": "timeout"}
    except Exception as exc:
        return {"return_code": -1, "stdout": "", "stderr": str(exc)}
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
        "delivery_kind": "inter_agent_message",
        "conversation_id": (action.get("conversation_id") or "local_run_command") + "_result",
        "from_agent": "AI Bridge Local Worker " + VERSION,
        "message": format_result_message(action, result, status)
    }

    try:
        post_json(f"{GATEWAY}/bridge/commands", body)
        print(f"[worker] Result enqueued: {result_command_id}")
    except Exception as e:
        print(f"[worker] Result enqueue skipped/error: {e}")

def format_accepted_message(action):
    command_id = action.get("command_id", "unknown")
    payload = action.get("payload", {}) if isinstance(action.get("payload", {}), dict) else {}
    cwd = payload.get("cwd", ".")
    return (
        "[AI_LOCAL]\n"
        "comando em execucao silenciosa\n"
        f"id={command_id}\n"
        "status=running\n"
        "no_reply=1\n"
        f"cwd={cwd}"
    )

def enqueue_accepted_message(action):
    source_chat_id = action.get("source_chat_id", "")
    if not source_chat_id:
        return ()

    command_id = action.get("command_id", "unknown")
    accepted_command_id = "accepted_to_" + command_id

    body = {
        "schema": "ai_bridge_local.envelope",
        "schema_version": 1,
        "command_id": accepted_command_id,
        "action": "send-chat-message",
        "source_chat_id": "gateway-brain-supervisor",
        "target_chat_id": source_chat_id,
        "delivery_kind": "inter_agent_message",
        "conversation_id": (action.get("conversation_id") or "local_run_command") + "_accepted",
        "from_agent": "AI Bridge Local Worker " + VERSION,
        "message": format_accepted_message(action),
    }

    try:
        post_json(f"{GATEWAY}/bridge/commands", body)
        print(f"[worker] Accepted notice enqueued: {accepted_command_id}")
    except Exception as e:
        print(f"[worker] Accepted notice skipped/error: {e}")



def run_action(action):
    command_id = action.get("command_id", "unknown")
    action_type = action.get("action", "")
    payload = action.get("payload", {})
    status = "acked"
    result = {"return_code": 0, "stdout": f"OK {action_type}", "stderr": ""}

    try:
        if action_type == "run-command":
            enqueue_accepted_message(action)
            cwd_key = normalize_cwd_for_lock(payload)
            cwd_lock = get_cwd_lock(cwd_key)
            print(f"[worker] Waiting cwd lock: {command_id} cwd={cwd_key}")
            with cwd_lock:
                print(f"[worker] Running with cwd lock: {command_id} cwd={cwd_key}")
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
            "error": result.get("stderr", "") if status == "failed" else "",
        }

        try:
            post_json(f"{GATEWAY}/bridge/acks", ack)
            print(f"[worker] {command_id}: {status}")
        except Exception as e:
            print(f"[worker] ACK error: {e}")
    except Exception as exc:
        print(f"[worker] run_action error for {command_id}: {exc}")

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
        enqueue_accepted_message(action)
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
    reap_run_futures()
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

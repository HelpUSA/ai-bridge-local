# -*- coding: utf-8 -*-
"""AI Bridge Local - Brain Worker v0.1.1"""
import json, subprocess, time, urllib.request

GATEWAY = "http://127.0.0.1:8766"

def now_iso():
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()

def post_json(url, data, timeout=10):
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())

def get_json(url, timeout=10):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read())

def execute_command(payload):
    cmd = payload.get("command", [])
    cwd = payload.get("cwd", ".")
    timeout = payload.get("timeout_seconds", 30)
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, shell=False)
        return {"return_code": result.returncode, "stdout": result.stdout[:5000], "stderr": result.stderr[:5000]}
    except subprocess.TimeoutExpired:
        return {"return_code": -1, "stdout": "", "stderr": "timeout"}
    except Exception as e:
        return {"return_code": -1, "stdout": "", "stderr": str(e)}

def poll_once():
    try:
        data = get_json(f"{GATEWAY}/bridge/next-action?chat_id=gateway-brain-supervisor")
    except Exception as e:
        print(f"[worker] Poll error: {e}"); return
    action = data.get("action") if data else None
    if not action: return
    command_id = action.get("command_id", "unknown")
    action_type = action.get("action", "")
    payload = action.get("payload", {})
    if action_type == "send-chat-message":
        print(f"[worker] Skip {command_id} (send-chat-message - extension handles)")
        return
    print(f"[worker] Running: {command_id} ({action_type})")
    if action_type == "run-command":
        result = execute_command(payload)
        status = "acked" if result["return_code"] == 0 else "failed"
    else:
        result = {"return_code": 0, "stdout": f"OK {action_type}", "stderr": ""}
        status = "acked"
    ack = {"command_id": command_id, "status": status, "return_code": result["return_code"], "stdout": result.get("stdout", ""), "stderr": result.get("stderr", ""), "error": result.get("stderr", "") if status == "failed" else ""}
    try:
        post_json(f"{GATEWAY}/bridge/acks", ack)
        print(f"[worker] {command_id}: {status}")
    except Exception as e:
        print(f"[worker] ACK error: {e}")

def main():
    print("[worker] AI Bridge Local Worker v0.1.1 - Porta 8766")
    print("[worker] Ctrl+C to stop")
    while True:
        try: poll_once()
        except Exception as e: print(f"[worker] Loop error: {e}")
        time.sleep(2)

if __name__ == "__main__": main()

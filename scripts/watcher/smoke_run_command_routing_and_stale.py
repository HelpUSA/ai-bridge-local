from pathlib import Path

gateway = Path("gateway_local.py").read_text(encoding="utf-8")

checks = {
    "run-command local_capability normalized body target": 'body["target_chat_id"] = "gateway-brain-supervisor"' in gateway,
    "run-command normalization condition": 'body.get("action") == "run-command"' in gateway and 'body.get("delivery_kind") == "local_capability"' in gateway,
    "misrouted stale run-command detected": "target_chat_id!='gateway-brain-supervisor'" in gateway,
    "stale run-command final result": "stale_run_command_timeout" in gateway and "result_to_" in gateway,
    "stale run-command next action": "fix_run_command_routing" in gateway,
}

missing = [name for name, ok in checks.items() if not ok]
if missing:
    raise SystemExit("Missing run-command routing/stale markers: " + ", ".join(missing))

print("OK run_command_routing_and_stale_smoke")

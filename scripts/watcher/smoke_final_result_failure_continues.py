
from pathlib import Path
import importlib.util

path = Path("brain_worker.py")
text = path.read_text(encoding="utf-8")

required_static = [
    'success = "1" if status == "acked" and return_code == 0 else "0"',
    'chat_can_continue = "1"',
    'next_action = "continue_next_activity" if success == "1" else "fix_error_before_continue"',
    'f"success={success}\\n"',
    'f"chat_can_continue={chat_can_continue}\\n"',
    'Comando falhou. O chat deve analisar stderr/stdout',
]

for marker in required_static:
    assert marker in text, marker

assert 'chat_can_continue = "1" if status == "acked"' not in text

spec = importlib.util.spec_from_file_location("brain_worker_smoke", path)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

ok_msg = module.format_result_message(
    {"command_id": "ok_cmd", "payload": {"cwd": ".", "command": ["echo", "ok"]}},
    {"return_code": 0, "stdout": "ok", "stderr": ""},
    "acked",
)
assert "result_is_final=1" in ok_msg
assert "success=1" in ok_msg
assert "chat_can_continue=1" in ok_msg
assert "next_action=continue_next_activity" in ok_msg

fail_msg = module.format_result_message(
    {"command_id": "fail_cmd", "payload": {"cwd": ".", "command": ["bad"]}},
    {"return_code": 1, "stdout": "", "stderr": "boom"},
    "failed",
)
assert "result_is_final=1" in fail_msg
assert "success=0" in fail_msg
assert "chat_can_continue=1" in fail_msg
assert "next_action=fix_error_before_continue" in fail_msg
assert "Comando falhou" in fail_msg

print("OK final_result_failure_continues_smoke")

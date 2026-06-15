
from pathlib import Path
import re

text = Path("brain_worker.py").read_text(encoding="utf-8")

assert "result_is_final=1" in text
assert "chat_can_continue" in text
assert "continue_next_activity" in text

fmt = re.search(r"(?ms)^def format_accepted_message\(action\):.*?(?=^def )", text)
assert fmt, "format_accepted_message block not found"
fmt_block = fmt.group(0)
assert 'return ""' in fmt_block
assert "[AI_LOCAL]" not in fmt_block
assert "status=running" not in fmt_block

accepted = re.search(r"(?ms)^def enqueue_accepted_message\(action\):.*?(?=^def )", text)
assert accepted, "enqueue_accepted_message block not found"
accepted_block = accepted.group(0)
assert "return None" in accepted_block
assert "[AI_LOCAL]" not in accepted_block
assert "status=running" not in accepted_block
assert "accepted_to_" not in accepted_block
assert "insert_command" not in accepted_block

calls = re.findall(r"(?m)^\s*enqueue_accepted_message\(action\)\s*$", text)
assert not calls, calls

print("OK remove_accepted_running_notice_smoke")

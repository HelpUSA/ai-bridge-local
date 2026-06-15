
from pathlib import Path

text = Path("brain_worker.py").read_text(encoding="utf-8")

required = [
    "result_is_final=1",
    "chat_can_continue",
    "continue_next_activity",
    "fix_error_before_continue",
    "Comando concluido com sucesso",
    "Comando falho",
]
for marker in required:
    assert marker in text, marker

assert text.count("result_is_final=1") == 1
assert text.count("next_action=") >= 1

print("OK final_result_continue_hint_smoke")

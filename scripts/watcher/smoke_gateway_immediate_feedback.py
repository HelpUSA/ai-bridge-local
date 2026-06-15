
from pathlib import Path

text = Path("gateway_local.py").read_text(encoding="utf-8")
assert "def enqueue_source_feedback" in text
assert "tipo=invalid_envelope" in text
assert "status=queued" in text
assert "Nao precisa responder" in text
assert "enqueue_source_feedback(body, 'invalid_envelope', validation_error)" in text
assert "enqueue_source_feedback(body, 'accepted', 'queued')" in text
assert "body.get('action') != 'run-command'" in text
print("OK gateway_immediate_feedback_smoke")

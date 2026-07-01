
from pathlib import Path

text = Path("gateway_local.py").read_text(encoding="utf-8")
assert "def enqueue_source_feedback" in text
assert "tipo=invalid_envelope" in text
assert "status=queued" in text
assert "Evento intermediario" in text
assert "enqueue_source_feedback(body, 'invalid_envelope', validation_error)" in text
assert "enqueue_source_feedback(body, 'accepted', 'queued')" in text
assert "Emit accepted/queued feedback for both run-command and send-chat-message." in text
assert "body.get('action') != 'run-command'" not in text
print("OK gateway_immediate_feedback_smoke")
assert "original_id.startswith(\'local_status_\')" in text

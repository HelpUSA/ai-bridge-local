
from pathlib import Path

gateway = Path("gateway_local.py").read_text(encoding="utf-8")
assert "def enqueue_source_feedback" in gateway
assert "tipo=invalid_envelope" in gateway
assert "status=queued" in gateway
assert "_to_" in gateway
assert "source_key =" in gateway
assert "uuid.uuid4().hex[:12]" not in gateway
assert "claim_lost" in gateway or "UPDATE commands SET status='delivering', delivered_at=? WHERE command_id=? AND status='queued'" in gateway

worker_path = Path("brain_worker.py")
if worker_path.exists():
    worker = worker_path.read_text(encoding="utf-8")
    assert "comando aceito, execucao iniciada" not in worker

print("OK gateway_feedback_dedup_smoke")

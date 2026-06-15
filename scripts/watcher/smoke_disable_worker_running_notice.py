
from pathlib import Path

worker = Path("brain_worker.py").read_text(encoding="utf-8")
assert "comando aceito, execucao iniciada" not in worker
assert "comando em execucao silenciosa" not in worker

for js_name in ["extension/background.js", "extension/content_script.js"]:
    p = Path(js_name)
    if p.exists():
        text = p.read_text(encoding="utf-8")
        assert "0.5.5" in text or js_name.endswith("content_script.js")

print("OK disable_worker_running_notice_smoke")

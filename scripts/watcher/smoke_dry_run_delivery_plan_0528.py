from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "watcher"))

from dry_run_delivery_plan import (  # noqa: E402
    build_dry_run_delivery_plan,
    render_dry_run_delivery_plan,
)

version_bytes = (ROOT / "VERSION").read_bytes()
assert not version_bytes.startswith(b"\xef\xbb\xbf"), version_bytes
VERSION = version_bytes.decode("utf-8").strip()
assert VERSION == "0.5.28", VERSION

manifest = json.loads((ROOT / "extension" / "manifest.json").read_text(encoding="utf-8-sig"))
assert manifest["version"] == VERSION, manifest
assert VERSION in manifest["name"], manifest["name"]

request = {
    "command_id": "dry-run-001",
    "source_chat_id": "source-1",
    "target_chat_id": "target-1",
    "target_registered": True,
    "target_tab_open": True,
    "composer_available": True,
    "composer_empty": True,
    "send_button_enabled": True,
    "blocking_modal": False,
    "payload": "hello dry run",
    "manual_authorization": True,
}

plan = build_dry_run_delivery_plan(request)
assert plan["readonly"] is True
assert plan["will_send"] is False
assert plan["preflight"]["allowed"] is True
assert "ready_for_separate_guarded_delivery" in plan["actions"]
assert plan["risk"] == "low_readonly"

blocked = dict(request)
blocked["target_tab_open"] = False
blocked_plan = build_dry_run_delivery_plan(blocked)
assert blocked_plan["will_send"] is False
assert blocked_plan["preflight"]["allowed"] is False
assert "stop_before_delivery" in blocked_plan["actions"]
assert blocked_plan["risk"] == "blocked_by_preflight"

rendered = render_dry_run_delivery_plan(plan)
assert "# Dry-run delivery plan" in rendered
assert "readonly=true" in rendered
assert "will_send=false" in rendered
assert "Does not send messages." in rendered

doc = (ROOT / "docs" / "DRY_RUN_DELIVERY_PLAN_0528.md").read_text(encoding="utf-8-sig")
guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")
assert "Dry-run delivery plan 0.5.28" in doc
assert "Nunca executa entrega inter-chat" in doc
assert "Version alignment 0.5.28" in guide
assert "Preflight dry-run batch 0.5.28" in guide
assert "v0.5.28-preflight-dry-run-batch" in guide

print("OK dry_run_delivery_plan_0528 0.5.28")
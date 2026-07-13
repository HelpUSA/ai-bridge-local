#!/usr/bin/env python3
from pathlib import Path

def main() -> int:
    print("SMOKE_GATEWAY_ROUTE_POLICY_DIAGNOSTICS_START", flush=True)
    gateway = Path("gateway_local.py").read_text(encoding="utf-8")
    control_center = Path("app_windows/control_center_app.py").read_text(encoding="utf-8")
    for marker in [
        "def get_gateway_route_policy():",
        "def decide_gateway_route(",
        "route_policy=get_gateway_route_policy()",
        'mode="gateway_first"',
        "direct_interchat_enabled=False",
        'direct_interchat_disabled_reason="gateway_first_control_plane_owns_delivery"',
        'blocked_route="direct_interchat"',
        'replacement_route="local_gateway"',
        'inter_agent_message_route="local_gateway"',
        'local_capability_route="local_gateway"',
        'decision_owner="gateway_control_plane"',
        'extension_role="thin_transport_executor"',
    ]:
        assert marker in gateway, marker
    for marker in [
        'policy = data.get("route_policy", {})',
        "Politica de rota: ",
        "Direct interchat: ",
        "Inter-agent route: ",
        "Local capability route: ",
        "Route lock: ",
    ]:
        assert marker in control_center, marker
    print("SMOKE_GATEWAY_ROUTE_POLICY_DIAGNOSTICS_OK", flush=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

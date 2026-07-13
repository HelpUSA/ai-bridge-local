#!/usr/bin/env python3
"""Smoke tests for executable gateway route decisions."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import gateway_local


def main() -> int:
    print("SMOKE_GATEWAY_ROUTE_DECISION_START", flush=True)

    policy = gateway_local.get_gateway_route_policy()
    assert policy["mode"] == "gateway_first"
    assert policy["direct_interchat_enabled"] is False
    assert policy["blocked_route"] == "direct_interchat"
    assert policy["replacement_route"] == "local_gateway"

    inter_agent = gateway_local.decide_gateway_route({
        "action": "send-chat-message",
        "delivery_kind": "inter_agent_message",
        "source_chat_id": "source-chat",
        "target_chat_id": "destination-chat",
    })
    assert inter_agent["route"] == "local_gateway"
    assert inter_agent["target_chat_id"] == "destination-chat"
    assert inter_agent["executor_role"] == "thin_transport_executor"
    assert inter_agent["reason"] == "gateway_first_inter_agent_delivery"

    local_capability = gateway_local.decide_gateway_route({
        "action": "run-command",
        "delivery_kind": "local_capability",
        "source_chat_id": "source-chat",
        "target_chat_id": "incorrect-target",
    })
    assert local_capability["route"] == "local_gateway"
    assert local_capability["original_target_chat_id"] == "incorrect-target"
    assert local_capability["target_chat_id"] == "gateway-brain-supervisor"
    assert local_capability["executor_role"] == "local_capability_executor"

    blocked = gateway_local.decide_gateway_route(
        {
            "action": "send-chat-message",
            "delivery_kind": "inter_agent_message",
            "source_chat_id": "source-chat",
            "target_chat_id": "destination-chat",
        },
        {"requested_route": "direct_interchat"},
    )
    assert blocked["blocked_route"] == "direct_interchat"
    assert blocked["replacement_route"] == "local_gateway"
    assert blocked["route"] == "local_gateway"
    assert blocked["target_chat_id"] == "destination-chat"

    try:
        gateway_local.decide_gateway_route({"delivery_kind": "unsupported"})
    except ValueError as exc:
        assert str(exc) == "bad_delivery_kind"
    else:
        raise AssertionError("unsupported delivery kind must fail")

    source = open("gateway_local.py", encoding="utf-8").read()
    assert 'if self.path == "/control/route-policy":' in source
    assert 'if self.path == "/control/route-decision":' in source
    assert 'route_decision = decide_gateway_route(body, payload)' in source
    assert '"route_decision": route_decision' in source

    print("SMOKE_GATEWAY_ROUTE_DECISION_OK", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

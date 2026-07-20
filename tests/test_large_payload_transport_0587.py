from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

import gateway_command_plane as command_plane


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(
        encoding="utf-8"
    )


def test_release_version_alignment() -> None:
    manifest = json.loads(
        read("extension/manifest.json")
    )

    assert manifest["version"] == "0.5.87"
    assert manifest["name"] == "AI Bridge Local 0.5.87"

    active_files = [
        "app_windows/control_center_app.py",
        "brain_worker.py",
        "extension/background.js",
        "extension/content_script.js",
        "extension/manifest.json",
        "gateway_command_plane.py",
        "gateway_local.py",
        "queue_adapter.py",
        "scripts/smoke/smoke_gateway_command_plane_0585.py",
        "scripts/smoke/smoke_gateway_control_diagnostics.py",
        "tests/test_watcher_target_registry_0586.py",
    ]

    for relative_path in active_files:
        text = read(relative_path)
        assert "0.5.87" in text
        assert "0.5.86" not in text


def test_browser_large_payload_contract() -> None:
    background = read(
        "extension/background.js"
    )

    assert (
        "M12_LARGE_PAYLOAD_TRANSPORT_0587:START"
        in background
    )
    assert (
        "AI_BRIDGE_M12_INLINE_LIMIT_BYTES = 32768"
        in background
    )
    assert "/v1/payloads" in background
    assert "payload_ref" in background
    assert (
        "async function "
        "aiBridgePostCommandInline0586(cmd)"
        in background
    )
    assert "async function postCommand(cmd)" in background


def test_command_plane_payload_foundation() -> None:
    source = read(
        "gateway_command_plane.py"
    )

    assert command_plane.VERSION == "0.5.87"
    assert "MAX_INLINE=32768" in source
    assert 'path=="/v1/payloads"' in source
    assert "bridge2_payloads" in source
    assert "payload_ref" in source


def test_command_plane_payload_round_trip() -> None:
    serialized = json.dumps(
        {
            "script_text": "x" * 40000,
            "mode": "m12",
        },
        separators=(",", ":"),
    )

    with TemporaryDirectory() as temporary:
        store = command_plane.Store(
            Path(temporary) / "queue.db"
        )

        created = store.put_payload(
            serialized,
            encoding="utf-8",
        )

        payload_ref = created["payload_ref"]

        assert payload_ref.startswith("sha256:")
        assert len(payload_ref) == 71
        assert created["size_bytes"] == len(
            serialized.encode("utf-8")
        )

        stored = store.payload(payload_ref)

        assert stored is not None
        assert stored["content"] == serialized
        assert stored["encoding"] == "utf-8"


def test_legacy_boundary_remains_separate() -> None:
    assert "payload_ref" not in read(
        "gateway_local.py"
    )
    assert "payload_ref" not in read(
        "queue_adapter.py"
    )
    assert "payload_ref" not in read(
        "brain_worker.py"
    )


def test_m12_documentation_contract() -> None:
    required_markers = {
        "docs/AI_BRIDGE_LOCAL_GUIDE.md":
            "M12_LARGE_PAYLOAD_TRANSPORT_0587",
        "docs/architecture/gateway-command-plane.md":
            "M12_LARGE_PAYLOAD_TRANSPORT_0587",
        "docs/how-to/compact-gateway-commands.md":
            "M12_BROWSER_LARGE_PAYLOAD_0587",
        "docs/reference/smoke-test-matrix.md":
            "M12_LARGE_PAYLOAD_TRANSPORT_0587",
        "docs/roadmap/ai-bridge-local-gateway-first-roadmap.md":
            "M12_LARGE_PAYLOAD_TRANSPORT_0587",
    }

    for relative_path, marker in required_markers.items():
        assert marker in read(relative_path)

    status = read(
        "docs/status/"
        "2026-07-20-ai-bridge-local-"
        "0.5.87-m12-large-payload-transport.md"
    )

    assert (
        "safe transport for large command payloads"
        in status
    )

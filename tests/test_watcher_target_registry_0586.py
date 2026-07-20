import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONTENT = ROOT / "extension" / "content_script.js"
BACKGROUND = ROOT / "extension" / "background.js"

MANIFEST = ROOT / "extension" / "manifest.json"

DELIVERY_SMOKE = (
    ROOT
    / "scripts"
    / "smoke"
    / "smoke_watcher_delivery_policy_0585.js"
)

REGISTRY_SMOKE = (
    ROOT
    / "scripts"
    / "smoke"
    / "smoke_watcher_target_registry_0586.js"
)

DOCS = (
    ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md",
    ROOT
    / "docs"
    / "reference"
    / "smoke-test-matrix.md",
    ROOT
    / "docs"
    / "roadmap"
    / "ai-bridge-local-gateway-first-roadmap.md",
    ROOT
    / "docs"
    / "status"
    / "2026-07-17-ai-bridge-local-m11-watcher-delivery-audit.md",
)


def read(path: Path) -> str:
    return path.read_text(
        encoding="utf-8-sig"
    )


def test_content_heartbeat_contract() -> None:
    source = read(CONTENT)

    assert (
        "M11_CHAT_REGISTRATION_0586:START"
        in source
    )

    assert "AI_BRIDGE_CHAT_HEARTBEAT" in source
    assert "extractChatIdFromCurrentUrl" in source
    assert "5000" in source


def test_background_registry_contract() -> None:
    source = read(BACKGROUND)

    assert (
        "M11_TARGET_REGISTRY_0586:START"
        in source
    )

    assert "aiBridgeM11ChatRegistry" in source
    assert "chat_registration_heartbeat" in source


def test_exact_target_resolution_contract() -> None:
    source = read(BACKGROUND)

    assert "aiBridgeM11ResolveExactTargetTab" in source
    assert "target_chat_tab_not_found" in source
    assert "target_chat_tab_ambiguous" in source


def test_retry_wrapper_uses_resolved_tab() -> None:
    source = read(BACKGROUND)

    begin = source.index(
        "M11_BACKGROUND_RETRY_0585:START"
    )

    finish = source.index(
        "M11_BACKGROUND_RETRY_0585:END"
    )

    block = source[begin:finish]

    assert "aiBridgeM11ResolveExactTargetTab" in block
    assert "resolvedTabId" in block
    assert "injectText(" in block


def test_delivery_smoke_has_target_stub() -> None:
    source = read(DELIVERY_SMOKE)

    assert (
        "M11_RETRY_SMOKE_TARGET_STUB_0586:START"
        in source
    )

    assert (
        "aiBridgeM11ResolveExactTargetTab"
        in source
    )


def test_registry_smoke_and_docs() -> None:
    assert REGISTRY_SMOKE.is_file()

    assert (
        "SMOKE_WATCHER_TARGET_REGISTRY_0586_OK"
        in read(REGISTRY_SMOKE)
    )

    for path in DOCS:
        assert (
            "M11_TARGET_REGISTRATION_REPAIR_0586"
            in read(path)
        )


def test_release_version_0586() -> None:
    manifest = json.loads(
        MANIFEST.read_text(
            encoding="utf-8-sig"
        )
    )

    assert manifest["version"] == "0.5.86"
    assert manifest["name"] == "AI Bridge Local 0.5.86"

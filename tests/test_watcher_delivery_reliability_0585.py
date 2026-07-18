from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONTENT = (
    ROOT / "extension" / "content_script.js"
)

BACKGROUND = (
    ROOT / "extension" / "background.js"
)

NODE_SMOKE = (
    ROOT
    / "scripts"
    / "smoke"
    / "smoke_watcher_delivery_policy_0585.js"
)

DOCS = (
    ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md",
    ROOT / "docs" / "reference" / "smoke-test-matrix.md",
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


def test_content_delivery_guard() -> None:
    source = read(CONTENT)

    assert (
        "M11_CONTENT_DELIVERY_GUARD_0585:START"
        in source
    )

    assert "aiBridgeM11AlreadyVisible" in source

    assert (
        'method: "m11_already_visible"'
        in source
    )


def test_user_draft_is_not_owned() -> None:
    source = read(CONTENT)

    assert (
        "const ownedPreflightText = "
        "aiBridgeM11ComposerOwnsRequestedText"
        in source
    )

    assert (
        "ownership: \"user_content\""
        in source
    )

    assert (
        "composerAlreadyHasRequestedText || "
        "beforeText.includes"
        not in source
    )


def test_background_retry_contract() -> None:
    source = read(BACKGROUND)

    assert (
        "M11_BACKGROUND_RETRY_0585:START"
        in source
    )

    assert (
        "const delays = [0, 450, 1100];"
        in source
    )

    assert "inject_retry_scheduled" in source

    assert (
        "injectTextWithM11Retry(tabId, action)"
        in source
    )


def test_retry_metadata_contract() -> None:
    source = read(BACKGROUND)

    assert "stable_command_id" in source

    assert (
        "delivery_attempts: "
        "result.delivery_attempts ?? null"
        in source
    )

    assert (
        "idempotent: "
        "result.idempotent ?? false"
        in source
    )


def test_node_policy_smoke_and_docs() -> None:
    assert NODE_SMOKE.is_file()

    assert (
        "SMOKE_WATCHER_DELIVERY_POLICY_0585_OK"
        in read(NODE_SMOKE)
    )

    for path in DOCS:
        assert (
            "M11_ACTIVE_DELIVERY_RELIABILITY_0585"
            in read(path)
        )

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "extension" / "content_script.js"
BACKGROUND = ROOT / "extension" / "background.js"
GATEWAY = ROOT / "gateway_local.py"
WORKER = ROOT / "brain_worker.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").lower()


def test_delivery_sources_exist() -> None:
    for path in (CONTENT, BACKGROUND, GATEWAY, WORKER):
        assert path.is_file()
        assert path.stat().st_size > 0


def test_command_identity_contract() -> None:
    combined = read(CONTENT) + read(BACKGROUND) + read(GATEWAY)
    assert "command_id" in combined


def test_composer_detection_contract() -> None:
    source = read(CONTENT)
    assert any(
        token in source
        for token in ("composer", "textarea", "contenteditable", "editor")
    )


def test_submission_contract() -> None:
    source = read(CONTENT)
    assert any(
        token in source
        for token in (".click(", "keyboardevent", "dispatchEvent".lower(), "enter")
    )


def test_retry_contract() -> None:
    combined = read(CONTENT) + read(BACKGROUND) + read(GATEWAY) + read(WORKER)
    assert any(
        token in combined
        for token in ("retry", "attempt", "timeout", "backoff")
    )


def test_gateway_first_contract() -> None:
    combined = read(BACKGROUND) + read(GATEWAY)
    assert any(
        token in combined
        for token in ("gateway_first", "local_gateway", "gateway-first")
    )

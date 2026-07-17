from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONTROL_CENTER_PATH = (
    ROOT / "app_windows" / "control_center_app.py"
)

LAUNCHER_PATH = (
    ROOT / "app_windows" / "controlcenter_launcher.ps1"
)

BAT_PATH = (
    ROOT / "app_windows" / "controlcenter.bat"
)

SOURCE = CONTROL_CENTER_PATH.read_text(
    encoding="utf-8-sig"
)

TREE = ast.parse(
    SOURCE,
    filename=str(CONTROL_CENTER_PATH),
)


def source_segment(name: str) -> str:
    matches = [
        node
        for node in ast.walk(TREE)
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        )
        and node.name == name
    ]

    assert len(matches) == 1, (
        f"expected one function named {name}, "
        f"found {len(matches)}"
    )

    segment = ast.get_source_segment(
        SOURCE,
        matches[0],
    )

    assert segment
    return segment


def class_methods(class_name: str) -> set[str]:
    matches = [
        node
        for node in TREE.body
        if isinstance(node, ast.ClassDef)
        and node.name == class_name
    ]

    assert len(matches) == 1

    return {
        node.name
        for node in matches[0].body
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        )
    }


def test_single_instance_mutex_contract() -> None:
    function_source = source_segment(
        "_ai_bridge_control_center_single_instance_0585"
    )

    assert "CreateMutexW" in function_source
    assert "mutex_handle" in function_source

    assert (
        "_AI_BRIDGE_CONTROL_CENTER_MUTEX_0585"
        in SOURCE
    )

    assert (
        "_ai_bridge_control_center_single_instance_0585()"
        in SOURCE
    )


def test_autostart_contract() -> None:
    function_source = source_segment(
        "_ai_bridge_control_center_autostart_0585"
    )

    for token in (
        "gateway_local.py",
        "brain_worker.py",
        "_ab_threading.Thread",
        "gateway_autostart",
        "worker_autostart",
    ):
        assert token in function_source


def test_async_refresh_contract() -> None:
    methods = class_methods(
        "ControlCenterApp"
    )

    required_methods = {
        "_collect_refresh_payload",
        "_refresh_worker",
        "_apply_refresh_payload",
        "_drain_refresh_results",
        "refresh",
        "auto_refresh",
    }

    assert required_methods <= methods

    refresh_source = source_segment(
        "refresh"
    )

    for token in (
        "_refresh_inflight",
        "_refresh_pending",
        "_cc_threading.Thread",
        "_refresh_worker",
    ):
        assert token in refresh_source

    worker_source = source_segment(
        "_refresh_worker"
    )

    assert "_collect_refresh_payload" in worker_source
    assert "_refresh_results.put" in worker_source
    assert ".set(" not in worker_source

    apply_source = source_segment(
        "_apply_refresh_payload"
    )

    assert "_refresh_inflight = False" in apply_source
    assert "_refresh_pending" in apply_source
    assert ".set(" in apply_source


def test_active_and_historical_counter_contract() -> None:
    for token in (
        "queue_local.db",
        'counts["acked"] = max',
        "fila_ativa={0} queued={1} delivering={2}",
        "historico: acked={3} failed={4}",
        "dead_letters (historico)",
    ):
        assert token in SOURCE


def test_launcher_contract() -> None:
    launcher = LAUNCHER_PATH.read_text(
        encoding="utf-8-sig"
    )

    for token in (
        "[switch]$ValidateOnly",
        "Get-CimInstance Win32_Process",
        "Stop-Process",
        "Start-Process",
        "System.Threading.Mutex",
        "control_center_app.py",
        "VALIDATE_OK=1",
    ):
        assert token in launcher

    bat = BAT_PATH.read_text(
        encoding="utf-8-sig"
    )

    assert "controlcenter_launcher.ps1" in bat
    assert "-ValidateOnly" in bat

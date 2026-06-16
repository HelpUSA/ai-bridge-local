from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]


class SafeOpsError(RuntimeError):
    pass


def run(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        args,
        cwd=str(ROOT),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and proc.returncode != 0:
        raise SafeOpsError(
            "command failed: "
            + " ".join(args)
            + "\nstdout:\n"
            + proc.stdout
            + "\nstderr:\n"
            + proc.stderr
        )
    return proc


def status_short() -> list[str]:
    proc = run(["git", "status", "--short"])
    return [line for line in proc.stdout.splitlines() if line.strip()]


def ensure_clean(allow_exact: Iterable[str] = ()) -> None:
    allowed = set(allow_exact)
    dirty = status_short()
    unexpected = [line for line in dirty if line not in allowed]
    if unexpected:
        raise SafeOpsError("unexpected dirty files: " + repr(unexpected))


def diff_check() -> None:
    run(["git", "diff", "--check"])


def smoke_docs() -> None:
    run(["python", "scripts/watcher/smoke_docs.py"])


def py_compile(paths: Iterable[str]) -> None:
    run(["python", "-m", "py_compile", *list(paths)])


def stage_exact(paths: Iterable[str]) -> None:
    items = list(paths)
    if not items:
        raise SafeOpsError("stage_exact received no paths")
    run(["git", "add", "--", *items])


def commit(message: str) -> None:
    if not message.strip():
        raise SafeOpsError("empty commit message")
    run(["git", "commit", "-m", message])


def push_main() -> None:
    run(["git", "push", "origin", "main"])


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.rstrip() + "\n", encoding="utf-8")

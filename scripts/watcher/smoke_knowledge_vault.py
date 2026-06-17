from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path.cwd()
KNOWLEDGE = ROOT / "knowledge"
WRITER = ROOT / "scripts" / "watcher" / "knowledge_writer.py"
SMOKE_NOTE = KNOWLEDGE / "tasks" / "smoke-knowledge-writer.md"


def check(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def main() -> None:
    required = [
        KNOWLEDGE / "00_HOME.md",
        KNOWLEDGE / "projects" / "ai-bridge-local" / "status.md",
        KNOWLEDGE / "templates" / "task.md",
        KNOWLEDGE / "templates" / "decision.md",
        KNOWLEDGE / "templates" / "error.md",
        KNOWLEDGE / "templates" / "smoke.md",
        KNOWLEDGE / "templates" / "release.md",
        KNOWLEDGE / "tasks" / ".gitkeep",
        KNOWLEDGE / "decisions" / ".gitkeep",
        KNOWLEDGE / "errors" / ".gitkeep",
        KNOWLEDGE / "smokes" / ".gitkeep",
        KNOWLEDGE / "releases" / ".gitkeep",
        WRITER,
    ]

    for path in required:
        check(path.exists(), "missing required path: " + str(path))

    home = (KNOWLEDGE / "00_HOME.md").read_text(encoding="utf-8-sig", errors="replace")
    status = (KNOWLEDGE / "projects" / "ai-bridge-local" / "status.md").read_text(
        encoding="utf-8-sig",
        errors="replace",
    )

    check("[[projects/ai-bridge-local/status]]" in home, "home missing status link")
    check("Smart Watcher base criada" in status, "status missing smart watcher marker")
    check("Knowledge Vault v1 iniciado" in status, "status missing vault marker")

    if SMOKE_NOTE.exists():
        SMOKE_NOTE.unlink()

    result = run(
        [
            "python",
            "scripts/watcher/knowledge_writer.py",
            "task",
            "--title",
            "Smoke Knowledge Writer",
            "--slug",
            "smoke-knowledge-writer",
            "--body",
            "Nota temporaria criada pelo smoke.",
            "--tags",
            "smoke,knowledge,ai-bridge-local",
        ]
    )

    check("knowledge/tasks/smoke-knowledge-writer.md" in result.stdout, "writer stdout mismatch")
    check(SMOKE_NOTE.exists(), "writer did not create smoke note")

    note = SMOKE_NOTE.read_text(encoding="utf-8-sig", errors="replace")
    check("# Smoke Knowledge Writer" in note, "note missing title")
    check("Tipo: task" in note, "note missing kind")
    check("[[../projects/ai-bridge-local/status]]" in note, "note missing project link")
    check("Nota temporaria criada pelo smoke." in note, "note missing body")

    SMOKE_NOTE.unlink()

    run(["python", "-m", "py_compile", "scripts/watcher/knowledge_writer.py"])

    print("OK smoke_knowledge_vault")


if __name__ == "__main__":
    main()

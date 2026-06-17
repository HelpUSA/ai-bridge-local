from __future__ import annotations

import argparse
import json
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable
from knowledge_writer import write_note

ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = ROOT / "runtime" / "smart_tasks"


class SmartWatcherError(RuntimeError):
    pass


def run_cmd(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
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
        raise SmartWatcherError(
            "command failed: "
            + " ".join(args)
            + "\nstdout:\n"
            + proc.stdout
            + "\nstderr:\n"
            + proc.stderr
        )
    return proc


def git_status_short() -> list[str]:
    proc = run_cmd(["git", "status", "--short"])
    return [line for line in proc.stdout.splitlines() if line.strip()]


def git_head() -> str:
    return run_cmd(["git", "log", "-1", "--oneline"]).stdout.strip()


def classify_failure(text: str) -> dict[str, object]:
    lower = (text or "").lower()

    patterns = [
        (
            "expected ','",
            "invalid_json",
            "Envelope JSON quebrado, geralmente por aspas internas em script_text.",
            "Reenviar como script local ou reduzir o envelope.",
            True,
        ),
        (
            "base64",
            "fragile_large_payload",
            "Payload grande ou base64 truncado/corrompido.",
            "Evitar base64 no chat; criar arquivo local.",
            True,
        ),
        (
            "new blank line at eof",
            "diff_check_failed",
            "git diff --check encontrou problema de espaco/EOF.",
            "Normalizar arquivo com uma unica quebra de linha final.",
            True,
        ),
        (
            "already exists",
            "idempotency_collision",
            "Operacao encontrou destino ja existente.",
            "Tratar estado parcial como esperado ou tornar a operacao idempotente.",
            True,
        ),
        (
            "syntaxerror",
            "script_syntax_error",
            "Script gerado tem erro de sintaxe.",
            "Salvar em arquivo local, compilar e so depois executar.",
            True,
        ),
        (
            "unexpected dirty",
            "dirty_repo",
            "Repo contem alteracoes fora da allowlist.",
            "Parar, inspecionar git status e continuar so com aprovacao.",
            False,
        ),
    ]

    for needle, category, cause, action, retryable in patterns:
        if needle in lower:
            return {
                "category": category,
                "likely_cause": cause,
                "recommended_action": action,
                "retryable": retryable,
            }

    return {
        "category": "unknown_failure",
        "likely_cause": "Nenhum padrao conhecido encontrado.",
        "recommended_action": "Inspecionar stdout, stderr e git status; repetir em etapa menor.",
        "retryable": False,
    }


@dataclass
class TaskStep:
    name: str
    action: Callable[[], str]
    completed: bool = False
    output: str = ""


@dataclass
class SmartTask:
    task_id: str
    objective: str
    steps: list[TaskStep] = field(default_factory=list)
    status: str = "planned"
    last_error: str = ""

    @property
    def state_path(self) -> Path:
        return STATE_DIR / f"{self.task_id}.json"

    def save(self) -> None:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        payload = {
            "task_id": self.task_id,
            "objective": self.objective,
            "status": self.status,
            "last_error": self.last_error,
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "steps": [
                {
                    "name": step.name,
                    "completed": step.completed,
                    "output": step.output,
                }
                for step in self.steps
            ],
        }
        self.state_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def run(self, dry_run: bool = False) -> None:
        self.status = "dry_run" if dry_run else "running"
        self.save()

        for step in self.steps:
            if step.completed:
                continue

            if dry_run:
                step.output = "planned"
                continue

            try:
                step.output = step.action()
                step.completed = True
                self.save()
            except Exception as exc:
                self.status = "failed"
                self.last_error = f"{type(exc).__name__}: {exc}"
                self.save()
                raise

        self.status = "planned" if dry_run else "completed"
        self.save()


 def write_knowledge_note(self, dry_run: bool = False) -> Path:
 related_files = [self.state_path.relative_to(ROOT).as_posix()]
 lines = [
 '# Smart Task Knowledge Note',
 '',
 '## Objective',
 self.objective,
 '',
 '## Status',
 self.status,
 '',
 '## Dry run',
 str(dry_run).lower(),
 '',
 '## Last error',
 self.last_error or 'none',
 '',
 '## Steps',
 ]
 for step in self.steps:
 lines.append(f'- {step.name}: completed={str(step.completed).lower()} output={step.output}')
 lines.extend(['', '## Related files'])
 for item in related_files:
 lines.append(f'- {item}')
 return write_note(
 'task',
 f'Smart task {self.task_id}',
 '
'.join(lines),
 slug=f'smart-task-{self.task_id}',
 tags=['ai-bridge-local', 'smart-task', 'knowledge-vault'],
 )

def demo_task(task_id: str) -> SmartTask:
    def inspect() -> str:
        return "repo_head=" + git_head()

    def plan() -> str:
        return "steps=inspect,plan,validate"

    def validate() -> str:
        dirty = git_status_short()
        if dirty:
            return "repo_dirty_allowed_for_demo=" + repr(dirty)
        return "repo_clean"

    return SmartTask(
        task_id=task_id,
        objective="Demonstrar execucao de tarefa em etapas com estado persistente.",
        steps=[
            TaskStep("inspect", inspect),
            TaskStep("plan", plan),
            TaskStep("validate", validate),
        ],
    )


def catalog() -> list[dict[str, object]]:
    return [
        {"task_id": "smart_watcher_demo", "title": "Smart Watcher demo", "mode": "dry_run_first", "risk": "low"},
        {"task_id": "docs_v0_update", "title": "Documentar modo v0 UI research", "mode": "report_only", "risk": "low"},
        {"task_id": "repo_status_report", "title": "Relatorio readonly de repo", "mode": "readonly", "risk": "low"},
        {"task_id": "release_validation", "title": "Validacao pre-release", "mode": "validate_only", "risk": "medium"},
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("task", nargs="?", default="demo")
    parser.add_argument("--task-id", default="smart_watcher_demo")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--catalog", action="store_true")
    parser.add_argument("--classify-error", default="")
    parser.add_argument("--json", action="store_true")
    parser.add_argument('--print-state', action='store_true')
 parser.add_argument('--no-knowledge', action='store_true')
    args = parser.parse_args()

    if args.catalog:
        print(json.dumps(catalog(), indent=2, ensure_ascii=False))
        return 0

    if args.classify_error:
        payload = classify_failure(args.classify_error)
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(payload["category"])
            print(payload["likely_cause"])
            print(payload["recommended_action"])
            print("retryable=" + str(payload["retryable"]).lower())
        return 0

    if args.task != "demo":
        raise SystemExit("unknown task: " + args.task)

    task = demo_task(args.task_id)
    task.run(dry_run=args.dry_run)
 if not args.no_knowledge:
 task.write_knowledge_note(dry_run=args.dry_run)

    if args.print_state:
        print(task.state_path.read_text(encoding="utf-8"))
    else:
        print(task.state_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


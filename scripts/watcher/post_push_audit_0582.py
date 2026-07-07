# -*- coding: utf-8 -*-
"""Standard short post-push audit for AI Bridge Local.

Python-only by design: avoids fragile inline PowerShell validation blocks.
Run this after a release commit has been pushed.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class AuditFailure(Exception):
    pass


class CheckResult:
    def __init__(self, name, code, stdout="", stderr=""):
        self.name = name
        self.code = code
        self.stdout = stdout
        self.stderr = stderr


def run(args, name=None):
    label = name or " ".join(args)
    proc = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    return CheckResult(label, proc.returncode, proc.stdout, proc.stderr)


def emit(check):
    print(f"RUN {check.name}")
    if check.stdout:
        print(check.stdout, end="" if check.stdout.endswith("\n") else "\n")
    if check.stderr:
        print(check.stderr, end="" if check.stderr.endswith("\n") else "\n")
    print(f"RC={check.code}")


def must_pass(check):
    emit(check)
    if check.code != 0:
        raise AuditFailure(f"{check.name} failed with rc={check.code}")


def git_status_line():
    check = run(["git", "status", "-sb"], "git status -sb")
    if check.code != 0:
        emit(check)
        raise AuditFailure("git status failed")
    return check.stdout.strip()


def assert_clean_synced_status(status_line):
    print("STATUS")
    print(status_line)
    lines = [line for line in status_line.splitlines() if line.strip()]
    if len(lines) != 1:
        raise AuditFailure("worktree not clean: git status has more than one line")
    header = lines[0]
    lower = header.lower()
    if "[ahead" in lower or "[behind" in lower:
        raise AuditFailure(f"branch not synced: {header}")
    if "..." not in header:
        raise AuditFailure(f"branch does not show upstream: {header}")


def files_exist(paths):
    missing = [path for path in paths if not (ROOT / path).exists()]
    if missing:
        raise AuditFailure("missing expected files: " + ", ".join(missing))


def maybe_run_script(path):
    if (ROOT / path).exists():
        must_pass(run(["python", path], path))


def main():
    print("AI_BRIDGE_LOCAL_POST_PUSH_AUDIT_0582_START")
    files_exist([
        "VERSION",
        "brain_worker.py",
        "gateway_local.py",
        "queue_adapter.py",
        "scripts/watcher/post_push_audit_0582.py",
        "scripts/watcher/smoke_0582_post_push_audit.py",
    ])

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    print("VERSION " + version)

    print("HEAD")
    must_pass(run(["git", "log", "-1", "--oneline"], "git log -1 --oneline"))
    assert_clean_synced_status(git_status_line())
    must_pass(run(["git", "diff", "--check"], "git diff --check"))
    must_pass(run([
        "python",
        "-m",
        "py_compile",
        "brain_worker.py",
        "gateway_local.py",
        "queue_adapter.py",
        "scripts/watcher/post_push_audit_0582.py",
        "scripts/watcher/smoke_0582_post_push_audit.py",
    ], "py_compile core"))

    maybe_run_script("scripts/watcher/smoke_0580_browser_actions_queue_adapter.py")
    maybe_run_script("scripts/watcher/smoke_0581_worker_supervisor.py")
    maybe_run_script("scripts/watcher/smoke_0582_post_push_audit.py")

    print("AUT0582_PASS")
    print("AI_BRIDGE_LOCAL_POST_PUSH_AUDIT_0582_END")


if __name__ == "__main__":
    main()

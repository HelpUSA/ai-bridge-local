#!/usr/bin/env python3
"""Generic post-push repository audit helper for AI Bridge Local."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def run(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, check=check)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a generic post-push repository audit.")
    parser.add_argument("--expect-file", action="append", default=[], help="File that must exist.")
    parser.add_argument("--allow-dirty", action="store_true", help="Do not fail on dirty working tree.")
    parser.add_argument("--skip-upstream", action="store_true", help="Skip upstream ahead/behind check.")
    args = parser.parse_args()

    root = Path.cwd()
    print("POST_PUSH_AUDITOR_START")
    print("ROOT=" + str(root))

    head = run(["git", "rev-parse", "--short", "HEAD"]).stdout.strip()
    branch = run(["git", "branch", "--show-current"]).stdout.strip()
    print("HEAD=" + head)
    print("BRANCH=" + branch)

    status = run(["git", "status", "--short"]).stdout
    print("STATUS_SHORT=" + repr(status))
    if status.strip() and not args.allow_dirty:
        raise SystemExit("working tree is dirty")

    for rel in args.expect_file:
        path = root / rel
        print("EXPECT_FILE=" + rel + " exists=" + str(path.exists()))
        if not path.exists():
            raise SystemExit("expected file missing: " + rel)

    if not args.skip_upstream:
        upstream = run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], check=False)
        if upstream.returncode == 0:
            upstream_name = upstream.stdout.strip()
            counts = run(["git", "rev-list", "--left-right", "--count", "HEAD..." + upstream_name]).stdout.strip()
            ahead, behind = [int(part) for part in counts.split()]
            print("UPSTREAM=" + upstream_name)
            print("AHEAD=" + str(ahead))
            print("BEHIND=" + str(behind))
            if ahead or behind:
                raise SystemExit("branch is not synchronized with upstream")
        else:
            print("UPSTREAM=none")

    print("POST_PUSH_AUDITOR_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

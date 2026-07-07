# -*- coding: utf-8 -*-
"""Smoke tests for post_push_audit_0582."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "watcher"))

import post_push_audit_0582 as audit


def expect_failure(fn, expected_text):
    try:
        fn()
    except audit.AuditFailure as exc:
        assert expected_text in str(exc), str(exc)
        return
    raise AssertionError("expected AuditFailure")


def main():
    audit.assert_clean_synced_status("## main...origin/main")
    expect_failure(
        lambda: audit.assert_clean_synced_status("## main...origin/main [ahead 1]"),
        "not synced",
    )
    expect_failure(
        lambda: audit.assert_clean_synced_status("## main...origin/main\n M VERSION"),
        "not clean",
    )
    expect_failure(
        lambda: audit.assert_clean_synced_status("## main"),
        "does not show upstream",
    )
    audit.emit(audit.CheckResult("fake", 0, "stdout", ""))
    print("SMOKE_0582_POST_PUSH_AUDIT_OK")


if __name__ == "__main__":
    main()

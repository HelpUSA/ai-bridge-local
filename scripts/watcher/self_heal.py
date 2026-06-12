# -*- coding: utf-8 -*-
"""
AI Bridge Local self-heal.

Dry-run by default.
Use --apply to:
- start missing gateway_local.py
- start missing brain_worker.py
- stop duplicate brain_worker.py processes for this repo, keeping oldest
- mark stale delivering commands as failed
- mark stale legacy/smoke queued send-chat-message commands as failed

This script intentionally does not delete rows.
"""

from __future__ import annotations

import argparse
import os
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.1.2"

ROOT = Path.cwd()
DB = ROOT / "queue_local.db"
GATEWAY = ROOT / "gateway_local.py"
WORKER = ROOT / "brain_worker.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def print_section(name: str) -> None:
    print()
    print("## " + name)


def run_capture(cmd: list[str], timeout: int = 20) -> tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except Exception as exc:
        return 999, "", repr(exc)


def win_processes() -> list[dict[str, str]]:
    if os.name != "nt":
        return []

    ps = (
        "Get-CimInstance Win32_Process | "
        "Where-Object { $PSItem.CommandLine -match 'gateway_local.py|brain_worker.py|AI-Bridge-Local-Control-Center' } | "
        "Select-Object ProcessId,Name,CreationDate,CommandLine | ConvertTo-Json -Compress"
    )
    rc, out, err = run_capture(["powershell", "-NoProfile", "-Command", ps], timeout=20)
    if rc != 0 or not out.strip():
        return []

    import json

    data = json.loads(out)
    if isinstance(data, dict):
        return [data]
    return data


def is_repo_process(proc: dict[str, str], script: Path) -> bool:
    cmd = str(proc.get("CommandLine") or "")
    return str(script) in cmd or str(script).replace("/", "\\") in cmd


def process_report() -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    items = win_processes()
    gateways = [p for p in items if is_repo_process(p, GATEWAY)]
    workers = [p for p in items if is_repo_process(p, WORKER)]
    controls = [p for p in items if str(p.get("Name") or "").lower() == "ai-bridge-local-control-center.exe"]
    return gateways, workers, controls


def start_python(script: Path, apply: bool) -> None:
    print("START_NEEDED|" + str(script))
    if not apply:
        print("DRY_RUN|would_start|" + str(script))
        return

    subprocess.Popen(
        [sys.executable, "-u", str(script)],
        cwd=str(ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    )
    print("APPLY|started|" + str(script))


def stop_pid(pid: int, apply: bool) -> None:
    print("STOP_NEEDED|pid=" + str(pid))
    if not apply:
        print("DRY_RUN|would_stop_pid|" + str(pid))
        return

    if os.name == "nt":
        rc, out, err = run_capture(["powershell", "-NoProfile", "-Command", "Stop-Process -Id " + str(pid) + " -Force"], timeout=20)
        print("APPLY|stop_pid|" + str(pid) + "|rc=" + str(rc))
        if out.strip():
            print(out.strip())
        if err.strip():
            print(err.strip())
    else:
        os.kill(pid, 15)
        print("APPLY|stop_pid|" + str(pid))


def heal_processes(apply: bool) -> None:
    print_section("process self-heal")

    gateways, workers, controls = process_report()

    print("gateway_count=" + str(len(gateways)))
    print("worker_count=" + str(len(workers)))
    print("control_center_count=" + str(len(controls)))

    for p in gateways:
        print("GATEWAY|" + str(p.get("ProcessId")) + "|" + str(p.get("CreationDate")))
    for p in workers:
        print("WORKER|" + str(p.get("ProcessId")) + "|" + str(p.get("CreationDate")))
    for p in controls:
        print("CONTROL|" + str(p.get("ProcessId")) + "|" + str(p.get("CreationDate")))

    if len(gateways) == 0:
        start_python(GATEWAY, apply)
    elif len(gateways) > 1:
        print("WARN|multiple_gateways_detected|manual_review_required")

    if len(workers) == 0:
        start_python(WORKER, apply)
    elif len(workers) > 1:
        keep = sorted(workers, key=lambda p: str(p.get("CreationDate") or ""))[0]
        keep_pid = int(keep.get("ProcessId"))
        print("KEEP_WORKER_PID=" + str(keep_pid))
        for p in workers:
            pid = int(p.get("ProcessId"))
            if pid != keep_pid:
                stop_pid(pid, apply)


def db_columns(con: sqlite3.Connection, table: str) -> list[str]:
    return [r[1] for r in con.execute("pragma table_info(" + table + ")").fetchall()]


def mark_failed(con: sqlite3.Connection, command_id: str, reason: str, apply: bool) -> None:
    print("MARK_FAILED_NEEDED|" + command_id + "|" + reason)
    if not apply:
        print("DRY_RUN|would_mark_failed|" + command_id)
        return

    con.execute(
        "update commands set status='failed', last_error=? where command_id=? and status in ('queued','delivering')",
        (reason, command_id),
    )
    con.execute(
        "insert into events(command_id, event_type, message, payload_json) values(?,?,?,?)",
        (command_id, "self_heal_mark_failed", reason, "{}"),
    )
    print("APPLY|marked_failed|" + command_id)


def heal_db(apply: bool, delivering_minutes: int, queued_minutes: int) -> None:
    print_section("db self-heal")

    if not DB.exists():
        print("db_missing=" + str(DB))
        return

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    tables = [r[0] for r in con.execute("select name from sqlite_master where type='table' order by name").fetchall()]
    print("tables=" + ",".join(tables))

    if "commands" not in tables:
        print("commands_table_missing")
        con.close()
        return

    counts = con.execute("select status, count(1) as n from commands group by status order by status").fetchall()
    for r in counts:
        print("STATUS|" + str(r["status"]) + "|" + str(r["n"]))

    stale_delivering = con.execute(
        "select command_id, created_at, action, delivery_kind, source_chat_id, target_chat_id "
        "from commands "
        "where status='delivering' and datetime(created_at) < datetime('now', ?) "
        "order by created_at asc",
        ("-" + str(delivering_minutes) + " minutes",),
    ).fetchall()

    for r in stale_delivering:
        reason = "self_heal: stale delivering older than " + str(delivering_minutes) + " minutes"
        print("STALE_DELIVERING|" + dict_to_line(r))
        mark_failed(con, r["command_id"], reason, apply)

    stale_queued = con.execute(
        "select command_id, created_at, action, delivery_kind, source_chat_id, target_chat_id "
        "from commands "
        "where status='queued' and datetime(created_at) < datetime('now', ?) "
        "order by created_at asc",
        ("-" + str(queued_minutes) + " minutes",),
    ).fetchall()

    for r in stale_queued:
        legacy = str(r["delivery_kind"]) == "local_inter_agent_message"
        smoke = str(r["target_chat_id"]) in ("smoke", "manual-result-smoke")
        if legacy or smoke:
            reason = "self_heal: stale queued legacy/smoke older than " + str(queued_minutes) + " minutes"
            print("STALE_QUEUED_CANDIDATE|" + dict_to_line(r))
            mark_failed(con, r["command_id"], reason, apply)
        else:
            print("STALE_QUEUED_REVIEW_ONLY|" + dict_to_line(r))

    if apply:
        con.commit()
    con.close()


def dict_to_line(row: sqlite3.Row) -> str:
    d = dict(row)
    return "|".join(str(k) + "=" + str(v) for k, v in d.items())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Apply self-heal actions. Default is dry-run.")
    ap.add_argument("--dry-run", action="store_true", help="Explicit dry-run mode. This is the default.")
    ap.add_argument("--delivering-minutes", type=int, default=90)
    ap.add_argument("--queued-minutes", type=int, default=90)
    args = ap.parse_args()

    print("AI_BRIDGE_LOCAL_SELF_HEAL")
    print("version=" + VERSION)
    print("root=" + str(ROOT))
    print("time_utc=" + now_utc())
    print("mode=" + ("apply" if args.apply else "dry-run"))

    heal_processes(args.apply)
    heal_db(args.apply, args.delivering_minutes, args.queued_minutes)

    print()
    print("AI_BRIDGE_LOCAL_SELF_HEAL_DONE")
    return 0


raise SystemExit(main())

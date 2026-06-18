# -*- coding: utf-8 -*-
"""Inspect local AI Bridge command status by command_id.

This is a read-only diagnostic helper. It checks queue_local.db and recent
gateway/worker logs to classify whether a command was received, executed,
enqueued as a result, and/or likely failed during final delivery.
"""
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path
from typing import Iterable

DB_PATH = Path("queue_local.db")
WORKER_LOG = Path("logs/control_center_worker.log")
GATEWAY_LOG = Path("logs/control_center_gateway.log")


def tail_text(path: Path, max_chars: int = 900_000) -> str:
    if not path.exists():
        return ""
    data = path.read_bytes()
    if len(data) > max_chars:
        data = data[-max_chars:]
    return data.decode("utf-8", errors="replace")


def matching_lines(path: Path, patterns: Iterable[str], limit: int = 80) -> list[str]:
    text = tail_text(path)
    if not text:
        return []
    pats = [p for p in patterns if p]
    rows: list[str] = []
    for idx, line in enumerate(text.splitlines(), 1):
        if any(p in line for p in pats):
            rows.append(f"{idx}: {line}")
    return rows[-limit:]


def print_rows_for_command(command_id: str) -> None:
    if not DB_PATH.exists():
        print("DB_MISSING", DB_PATH)
        return
    result_id = "result_to_" + command_id
    con = sqlite3.connect(f"file:{DB_PATH.as_posix()}?mode=ro", uri=True, timeout=10)
    con.row_factory = sqlite3.Row
    try:
        tables = [r[0] for r in con.execute("select name from sqlite_master where type='table' order by name")]
        print("DB_TABLES", "}".join(tables))
        if "commands" not in tables:
            print("COMMANDS_TABLE_MISSING")
            return
        cols = [r[1] for r in con.execute("pragma table_info(commands)")]
        wanted = [
            "id", "command_id", "status", "source_chat_id", "target_chat_id",
            "action", "delivery_kind", "created_at", "delivered_at", "acked_at",
            "return_code", "last_error", "stdout", "stderr",
        ]
        selected = [c for c in wanted if c in cols]
        sql = "select " + ",".join(selected) + " from commands where command_id in (?, ?) order by id"
        rows = list(con.execute(sql, (command_id, result_id)))
        print("DB_MATCH_COUNT", len(rows))
        for row in rows:
            print("DB_ROW_START")
            for key in selected:
                val = row[key]
                if val is None:
                    val = ""
                text = str(val)
                if key in {"stdout", "stderr"} and len(text) > 500:
                    text = text[:500] + "...[truncated]"
                print(f"{key}={text}")
            print("DB_ROW_END")
    finally:
        con.close()


def classify(command_id: str) -> None:
    result_id = "result_to_" + command_id
    worker_lines = matching_lines(WORKER_LOG, [command_id, result_id, "Result enqueued", "Result enqueue skipped", "HTTP Error 409"], limit=120)
    gateway_lines = matching_lines(GATEWAY_LOG, [command_id, result_id, "database is locked", "fail_stale_deliveries", "ConnectionAbortedError"], limit=120)

    print("WORKER_MATCH_LINES_START")
    for line in worker_lines:
        print(line)
    print("WORKER_MATCH_LINES_END")

    print("GATEWAY_MATCH_LINES_START")
    for line in gateway_lines:
        print(line)
    print("GATEWAY_MATCH_LINES_END")

    worker_text = "\n".join(worker_lines)
    gateway_text = "\n".join(gateway_lines)
    if "Running: " + command_id in worker_text and "Result enqueued: " + result_id in worker_text:
        print("CLASSIFICATION=EXECUTED_AND_RESULT_ENQUEUED")
    elif "Running: " + command_id in worker_text:
        print("CLASSIFICATION=EXECUTED_BUT_RESULT_ENQUEUE_NOT_CONFIRMED")
    elif command_id in gateway_text or command_id in worker_text:
        print("CLASSIFICATION=SEEN_IN_LOGS_BUT_EXECUTION_NOT_CONFIRMED")
    else:
        print("CLASSIFICATION=NOT_FOUND_IN_RECENT_LOG_TAIL")
    if "database is locked" in gateway_text:
        print("DELIVERY_RISK=GATEWAY_SQLITE_LOCK_SEEN")
    if "Result enqueue skipped" in worker_text or "HTTP Error 409" in worker_text:
        print("DELIVERY_RISK=RESULT_ENQUEUE_CONFLICT_SEEN")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--command-id", required=True)
    args = parser.parse_args()
    command_id = args.command_id.strip()
    print("COMMAND_STATUS_PROBE_START")
    print("COMMAND_ID", command_id)
    print("RESULT_ID", "result_to_" + command_id)
    print_rows_for_command(command_id)
    classify(command_id)
    print("COMMAND_STATUS_PROBE_END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

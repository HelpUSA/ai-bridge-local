# -*- coding: utf-8 -*-
"""Read-only diagnostic helper for AI Bridge Local command delivery state."""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path
from typing import Iterable

DB_PATH = Path("queue_local.db")
WORKER_LOG = Path("logs/control_center_worker.log")
GATEWAY_LOG = Path("logs/control_center_gateway.log")


def configure_stdio() -> None:
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def safe_text(value: object, max_len: int | None = None) -> str:
    if value is None:
        text = ""
    else:
        text = str(value)
    text = text.encode("utf-8", errors="replace").decode("utf-8", errors="replace")
    text = text.replace("\r", "\\r").replace("\n", "\\n")
    if max_len is not None and len(text) > max_len:
        return text[:max_len] + "...[truncated]"
    return text


def emit(*parts: object) -> None:
    text = " ".join(safe_text(part) for part in parts)
    try:
        print(text)
    except UnicodeEncodeError:
        data = (text + "\n").encode("utf-8", errors="replace")
        buffer = getattr(sys.stdout, "buffer", None)
        if buffer is not None:
            buffer.write(data)
            buffer.flush()
        else:
            sys.stdout.write(data.decode("utf-8", errors="replace"))


def tail_text(path: Path, max_bytes: int = 900_000) -> str:
    if not path.exists():
        return ""
    data = path.read_bytes()
    if len(data) > max_bytes:
        data = data[-max_bytes:]
    return data.decode("utf-8", errors="replace")


def matching_lines(path: Path, patterns: Iterable[str], limit: int = 80) -> list[str]:
    text = tail_text(path)
    if not text:
        return []
    needles = [p for p in patterns if p]
    rows: list[str] = []
    for index, line in enumerate(text.splitlines(), 1):
        if any(needle in line for needle in needles):
            rows.append(f"{index}: {line}")
    return rows[-limit:]


def db_rows_for_command(command_id: str) -> None:
    if not DB_PATH.exists():
        emit("DB_MISSING", DB_PATH)
        return
    result_id = "result_to_" + command_id
    conn = sqlite3.connect(f"file:{DB_PATH.as_posix()}?mode=ro", uri=True, timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        tables = [row[0] for row in conn.execute("select name from sqlite_master where type='table' order by name")]
        emit("DB_TABLES", ",".join(tables))
        if "commands" not in tables:
            emit("COMMANDS_TABLE_MISSING")
            return
        cols = [row[1] for row in conn.execute("pragma table_info(commands)")]
        wanted = ["id", "command_id", "status", "source_chat_id", "target_chat_id", "action", "delivery_kind", "created_at", "delivered_at", "acked_at", "return_code", "last_error", "stdout", "stderr"]
        selected = [col for col in wanted if col in cols]
        sql = "select " + ",".join(selected) + " from commands where command_id in (?, ?) order by id"
        rows = list(conn.execute(sql, (command_id, result_id)))
        emit("DB_MATCH_COUNT", len(rows))
        for row in rows:
            emit("DB_ROW_START")
            for key in selected:
                limit = 500 if key in {"stdout", "stderr"} else None
                emit(f"{key}={safe_text(row[key], limit)}")
            emit("DB_ROW_END")
    finally:
        conn.close()


def classify(command_id: str) -> None:
    result_id = "result_to_" + command_id
    worker_lines = matching_lines(WORKER_LOG, [command_id, result_id, "Result enqueued", "Result enqueue skipped", "HTTP Error 409"], limit=120)
    gateway_lines = matching_lines(GATEWAY_LOG, [command_id, result_id, "database is locked", "fail_stale_deliveries", "ConnectionAbortedError", "inject_timeout"], limit=120)
    emit("WORKER_MATCH_LINES_START")
    for line in worker_lines:
        emit(line)
    emit("WORKER_MATCH_LINES_END")
    emit("GATEWAY_MATCH_LINES_START")
    for line in gateway_lines:
        emit(line)
    emit("GATEWAY_MATCH_LINES_END")
    worker_text = "\n".join(worker_lines)
    gateway_text = "\n".join(gateway_lines)
    if ("Running: " + command_id) in worker_text and ("Result enqueued: " + result_id) in worker_text:
        emit("CLASSIFICATION=EXECUTED_AND_RESULT_ENQUEUED")
    elif ("Running: " + command_id) in worker_text:
        emit("CLASSIFICATION=EXECUTED_BUT_RESULT_ENQUEUE_NOT_CONFIRMED")
    elif command_id in gateway_text or command_id in worker_text:
        emit("CLASSIFICATION=SEEN_IN_LOGS_BUT_EXECUTION_NOT_CONFIRMED")
    else:
        emit("CLASSIFICATION=NOT_FOUND_IN_RECENT_LOG_TAIL")
    if "database is locked" in gateway_text:
        emit("DELIVERY_RISK=GATEWAY_SQLITE_LOCK_SEEN")
    if "Result enqueue skipped" in worker_text or "HTTP Error 409" in worker_text:
        emit("DELIVERY_RISK=RESULT_ENQUEUE_CONFLICT_SEEN")
    if "inject_timeout" in gateway_text:
        emit("DELIVERY_RISK=INJECT_TIMEOUT_SEEN")


def main() -> int:
    configure_stdio()
    parser = argparse.ArgumentParser()
    parser.add_argument("--command-id", required=True)
    args = parser.parse_args()
    command_id = args.command_id.strip()
    emit("COMMAND_STATUS_PROBE_START")
    emit("COMMAND_ID", command_id)
    emit("RESULT_ID", "result_to_" + command_id)
    db_rows_for_command(command_id)
    classify(command_id)
    emit("COMMAND_STATUS_PROBE_END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

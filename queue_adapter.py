# -*- coding: utf-8 -*-
"""Minimal QueueAdapter for AI Bridge Local 0.5.86.

Compatibility adapter over the existing gateway_local commands table.
Durable Queue v2 can expand this without changing callers.
"""

import json
import sqlite3
from datetime import datetime, timezone

DB_PATH = "queue_local.db"


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def open_db(db_path=None):
    conn = sqlite3.connect(db_path or DB_PATH, timeout=30)
    conn.execute("PRAGMA busy_timeout = 30000")
    return conn


def init_db(db_path=None):
    conn = open_db(db_path)
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS commands ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "command_id TEXT UNIQUE NOT NULL, "
            "source_chat_id TEXT, target_chat_id TEXT, action TEXT, delivery_kind TEXT, "
            "conversation_id TEXT, from_agent TEXT, message TEXT, payload_json TEXT, "
            "status TEXT DEFAULT 'queued', created_at TEXT DEFAULT (datetime('now')), "
            "delivered_at TEXT, acked_at TEXT, return_code INTEGER, stdout TEXT, stderr TEXT, "
            "last_error TEXT)"
        )
        conn.execute(
            "CREATE TABLE IF NOT EXISTS queue_heartbeats ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "subject_id TEXT UNIQUE NOT NULL, status TEXT, payload_json TEXT, "
            "last_seen_at TEXT DEFAULT (datetime('now')))"
        )
        conn.commit()
    finally:
        conn.close()


class QueueAdapter:
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_PATH
        init_db(self.db_path)

    def enqueue(self, command):
        command = dict(command or {})
        command_id = command["command_id"]
        payload = command.get("payload") if "payload" in command else command.get("payload_json", {})
        conn = open_db(self.db_path)
        try:
            conn.execute(
                "INSERT INTO commands "
                "(command_id,source_chat_id,target_chat_id,action,delivery_kind,conversation_id,from_agent,message,payload_json) "
                "VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    command_id,
                    command.get("source_chat_id", ""),
                    command.get("target_chat_id", ""),
                    command.get("action", ""),
                    command.get("delivery_kind", ""),
                    command.get("conversation_id", ""),
                    command.get("from_agent", ""),
                    command.get("message", ""),
                    json.dumps(payload or {}, ensure_ascii=False),
                ),
            )
            conn.commit()
            return {"ok": True, "command_id": command_id, "status": "queued"}
        except sqlite3.IntegrityError:
            return {"ok": False, "error": "duplicate", "command_id": command_id}
        finally:
            conn.close()

    def claim(self, target_chat_id, source_chat_id=None):
        conn = open_db(self.db_path)
        try:
            if source_chat_id:
                row = conn.execute(
                    "SELECT command_id,source_chat_id,target_chat_id,action,delivery_kind,conversation_id,from_agent,message,payload_json "
                    "FROM commands WHERE status='queued' AND target_chat_id=? AND source_chat_id=? ORDER BY id ASC LIMIT 1",
                    (target_chat_id, source_chat_id),
                ).fetchone()
            else:
                row = conn.execute(
                    "SELECT command_id,source_chat_id,target_chat_id,action,delivery_kind,conversation_id,from_agent,message,payload_json "
                    "FROM commands WHERE status='queued' AND target_chat_id=? ORDER BY id ASC LIMIT 1",
                    (target_chat_id,),
                ).fetchone()
            if not row:
                return None
            conn.execute(
                "UPDATE commands SET status='delivering', delivered_at=? WHERE command_id=? AND status='queued'",
                (now_iso(), row[0]),
            )
            conn.commit()
            try:
                payload = json.loads(row[8]) if row[8] else {}
            except Exception:
                payload = {}
            return {
                "command_id": row[0],
                "source_chat_id": row[1],
                "target_chat_id": row[2],
                "action": row[3],
                "delivery_kind": row[4],
                "conversation_id": row[5],
                "from_agent": row[6],
                "message": row[7],
                "payload": payload,
                "status": "delivering",
            }
        finally:
            conn.close()

    def ack(self, command_id, return_code=0, stdout="", stderr=""):
        conn = open_db(self.db_path)
        try:
            cur = conn.execute(
                "UPDATE commands SET status='acked', acked_at=?, return_code=?, stdout=?, stderr=?, last_error='' WHERE command_id=?",
                (now_iso(), return_code, stdout, stderr, command_id),
            )
            conn.commit()
            return cur.rowcount == 1
        finally:
            conn.close()

    def fail(self, command_id, error, return_code=-1):
        conn = open_db(self.db_path)
        try:
            cur = conn.execute(
                "UPDATE commands SET status='failed', acked_at=?, return_code=?, stderr=?, last_error=? WHERE command_id=?",
                (now_iso(), return_code, error, error, command_id),
            )
            conn.commit()
            return cur.rowcount == 1
        finally:
            conn.close()

    def heartbeat(self, subject_id, status="ok", payload=None):
        conn = open_db(self.db_path)
        try:
            conn.execute(
                "INSERT INTO queue_heartbeats (subject_id,status,payload_json,last_seen_at) VALUES (?,?,?,?) "
                "ON CONFLICT(subject_id) DO UPDATE SET status=excluded.status, payload_json=excluded.payload_json, last_seen_at=excluded.last_seen_at",
                (subject_id, status, json.dumps(payload or {}, ensure_ascii=False), now_iso()),
            )
            conn.commit()
            return {"ok": True, "subject_id": subject_id, "status": status}
        finally:
            conn.close()

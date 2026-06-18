# -*- coding: utf-8 -*-
"""AI Bridge Local - Gateway v0.2.3"""
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

HOST = "127.0.0.1"
PORT = 8766
DB_PATH = "queue_local.db"

def open_db():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute('PRAGMA busy_timeout = 30000')
    return conn
VERSION = "0.2.7"

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def init_db():
    conn = open_db()
    conn.execute("CREATE TABLE IF NOT EXISTS commands (id INTEGER PRIMARY KEY AUTOINCREMENT, command_id TEXT UNIQUE NOT NULL, source_chat_id TEXT, target_chat_id TEXT, action TEXT, delivery_kind TEXT, conversation_id TEXT, from_agent TEXT, message TEXT, payload_json TEXT, status TEXT DEFAULT 'queued', created_at TEXT DEFAULT (datetime('now')), delivered_at TEXT, acked_at TEXT, return_code INTEGER, stdout TEXT, stderr TEXT, last_error TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, command_id TEXT, event_type TEXT, message TEXT, payload_json TEXT, created_at TEXT DEFAULT (datetime('now')))")
    conn.execute("CREATE TABLE IF NOT EXISTS invalid_messages (id INTEGER PRIMARY KEY AUTOINCREMENT, source_chat_id TEXT, raw_text TEXT, error TEXT, created_at TEXT DEFAULT (datetime('now')) )")
    conn.execute("CREATE TABLE IF NOT EXISTS dead_letters (id INTEGER PRIMARY KEY AUTOINCREMENT, command_id TEXT, source_chat_id TEXT, target_chat_id TEXT, action TEXT, delivery_kind TEXT, payload_json TEXT, last_error TEXT, attempt_count INTEGER, failed_at TEXT DEFAULT (datetime('now')))")
    conn.commit()
    conn.close()

def validate_command_body(body, payload):
    need = ['schema', 'schema_version', 'command_id', 'action', 'source_chat_id', 'target_chat_id', 'delivery_kind']
    for k in need:
        if not body.get(k):
            return 'missing_' + k
    if body.get('schema') != 'ai_bridge_local.envelope':
        return 'bad_schema'
    if body.get('action') not in ['send-chat-message', 'run-command']:
        return 'bad_action'
    if body.get('delivery_kind') not in ['inter_agent_message', 'local_capability']:
        return 'bad_delivery_kind'
    if body.get('action') == 'send-chat-message' and not body.get('message'):
        return 'missing_message'
    if body.get('action') == 'run-command':
        if not isinstance(payload, dict):
            return 'bad_payload'
        if not payload.get('cwd'):
            return 'missing_payload_cwd'
        if 'timeout_seconds' in payload and not isinstance(payload.get('timeout_seconds'), int):
            return 'bad_timeout_seconds'
        if not payload.get('command') and not payload.get('script_text') and not payload.get('script_path') and not payload.get('intent'):
            return 'missing_payload_command_or_script'
    return ''

def record_invalid_message(body, error, raw_text=None):
    conn = open_db()
    try:
        conn.execute("INSERT INTO invalid_messages (source_chat_id, raw_text, error) VALUES (?, ?, ?)", (body.get('source_chat_id', ''), (raw_text if raw_text is not None else json.dumps(body, ensure_ascii=False)), error))
        conn.commit()
    finally:
        conn.close()

def record_dead_letter(body, payload, error, attempt_count=1):
    conn = open_db()
    try:
        conn.execute('INSERT INTO dead_letters (command_id, source_chat_id, target_chat_id, action, delivery_kind, payload_json, last_error, attempt_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (body.get('command_id', ''), body.get('source_chat_id', ''), body.get('target_chat_id', ''), body.get('action', ''), body.get('delivery_kind', ''), json.dumps(payload or {}, ensure_ascii=False), error, attempt_count))
        conn.commit()
    finally:
        conn.close()

def record_event(command_id=None, event_type=None, message=None, payload=None):
    if not event_type:
        return False
    sql = 'INSERT INTO events (command_id, event_type, message, payload_json) VALUES (?, ?, ?, ?)'
    params = (command_id, event_type, message, json.dumps(payload or {}, ensure_ascii=False))
    conn = open_db()
    try:
        conn.execute(sql, params)
        conn.commit()
    finally:
        conn.close()
    return True

def fail_stale_deliveries(max_age_seconds=45):
    """Fail stale deliveries and recover misrouted local run-command rows."""
    try:
        cutoff_expr = f"-{int(max_age_seconds)} seconds"
        conn = open_db()
        try:
            conn.execute(
                """
                UPDATE commands
                   SET status='failed',
                       acked_at=?,
                       last_error='stale delivering timeout after extension delivery',
                       stderr='stale delivering timeout after extension delivery'
                 WHERE status='delivering'
                   AND action IN ('send-message','send-chat-message')
                   AND delivered_at IS NOT NULL
                   AND datetime(substr(delivered_at, 1, 19)) < datetime('now', ?)
                """,
                (now_iso(), cutoff_expr),
            )

            stale_run_rows = conn.execute(
                """
                SELECT command_id, source_chat_id, target_chat_id, conversation_id
                  FROM commands
                 WHERE status='delivering'
                   AND action='run-command'
                   AND delivery_kind='local_capability'
                   AND target_chat_id!='gateway-brain-supervisor'
                   AND delivered_at IS NOT NULL
                   AND datetime(substr(delivered_at, 1, 19)) < datetime('now', ?)
                """,
                (cutoff_expr,),
            ).fetchall()

            for command_id, source_chat_id, target_chat_id, conversation_id in stale_run_rows:
                error = (
                    "stale_run_command_timeout: run-command was delivered to a chat tab "
                    "instead of gateway-brain-supervisor; route local_capability run-command "
                    "to gateway-brain-supervisor"
                )
                conn.execute(
                    """
                    UPDATE commands
                       SET status='failed',
                           acked_at=?,
                           return_code=-1,
                           stderr=?,
                           last_error=?
                     WHERE command_id=?
                    """,
                    (now_iso(), error, error, command_id),
                )

                if source_chat_id:
                    result_command_id = "result_to_" + str(command_id)
                    message = chr(10).join([
                        "[AI_LOCAL_RUN]",
                        "id=" + str(command_id),
                        "status=failed",
                        "return_code=-1",
                        "no_reply=1",
                        "result_is_final=1",
                        "success=0",
                        "chat_can_continue=1",
                        "next_action=fix_run_command_routing",
                        "observacao=Comando local ficou preso em delivering porque foi roteado para uma aba de chat, nao para gateway-brain-supervisor.",
                        "stdout=",
                        "stderr=" + error,
                    ])
                    try:
                        conn.execute(
                            "INSERT INTO commands (command_id,source_chat_id,target_chat_id,action,delivery_kind,conversation_id,from_agent,message,payload_json) VALUES (?,?,?,?,?,?,?,?,?)",
                            (
                                result_command_id,
                                "gateway-brain-supervisor",
                                source_chat_id,
                                "send-chat-message",
                                "inter_agent_message",
                                (conversation_id or "local_run_command") + "_stale_result",
                                "AI Bridge Local Gateway",
                                message,
                                "{}",
                            ),
                        )
                    except sqlite3.IntegrityError:
                        pass

            conn.commit()
        finally:
            conn.close()
    except Exception as e:
        print("[gateway] fail_stale_deliveries error:", e)


def fetch_control_status():
    fail_stale_deliveries()
    conn = open_db()
    try:
        rows = conn.execute("SELECT status, COUNT(1) FROM commands GROUP BY status").fetchall()
        recent = conn.execute("SELECT command_id, source_chat_id, target_chat_id, action, status, created_at, last_error FROM commands ORDER BY id DESC LIMIT 30").fetchall()
        events = conn.execute("SELECT command_id, event_type, message, created_at FROM events ORDER BY id DESC LIMIT 30").fetchall()
        return dict(
            ok=True,
            service="ai-bridge-local",
            version=VERSION,
            timestamp=now_iso(),
            command_status={(r[0] or ""): r[1] for r in rows},
            recent_commands=[dict(command_id=r[0], source_chat_id=r[1], target_chat_id=r[2], action=r[3], status=r[4], created_at=r[5], last_error=r[6]) for r in recent],
            recent_events=[dict(command_id=r[0], event_type=r[1], message=r[2], created_at=r[3]) for r in events],
        )
    finally:
        conn.close()


def enqueue_source_feedback(body, feedback_type, detail):
    source_chat_id = body.get('source_chat_id', '')
    if not source_chat_id:
        return
    original_id = str(body.get('command_id', 'unknown'))
    if original_id.startswith('local_status_'):
        return
    target_chat_id = body.get('target_chat_id', '')
    # Emit accepted/queued feedback for both run-command and send-chat-message.
    # Inter-chat messages need this too, otherwise capture/enqueue can appear silent
    # until the destination tab eventually polls and emits a delivery status.
    safe_id = ''.join(ch if ch.isalnum() or ch in '-_' else '_' for ch in original_id)[:80]
    source_key = ''.join(ch if ch.isalnum() or ch in '-_' else '_' for ch in source_chat_id)[:24]
    local_id = 'local_status_' + feedback_type + '_' + safe_id + '_to_' + source_key
    if feedback_type == 'accepted':
        lines = [
            '[AI_LOCAL]',
            'comando recebido pelo gateway',
            'id=' + original_id,
            'status=queued',
            'processamento=na_fila_local',
            'no_reply=1',
            'destino=' + target_chat_id,
            'observacao=O comando entrou na fila local e sera processado. Nao precisa responder a esta mensagem.',
        ]
    else:
        lines = [
            '[AI_LOCAL_ERRO]',
            'acao=corrija_e_reenvie',
            'no_reply=0',
            'executado=nao',
            'tipo=invalid_envelope',
            'versao=' + VERSION,
            'id_original=' + original_id,
            'chat_atual=' + source_chat_id,
            'origem=' + source_chat_id,
            'destino=' + target_chat_id,
            'erro=' + str(detail),
            'causa_provavel=Envelope parseou, mas faltam campos obrigatorios ou ha campos invalidos.',
            'correcao=Nada foi executado. Corrija o envelope e reenvie.',
        ]
    message = chr(10).join(lines)
    conn = open_db()
    try:
        conn.execute(
            "INSERT INTO commands (command_id,source_chat_id,target_chat_id,action,delivery_kind,conversation_id,from_agent,message,payload_json) VALUES (?,?,?,?,?,?,?,?,?)",
            (local_id, 'gateway-brain-supervisor', source_chat_id, 'send-chat-message', 'inter_agent_message', body.get('conversation_id', ''), 'AI Bridge Local Gateway', message, '{}')
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

def normalize_payload(body):
    payload = body.get("payload", {})
    if not isinstance(payload, dict):
        payload = {}

    for key in ["command", "cwd", "timeout_seconds", "env"]:
        if key in body and key not in payload:
            payload[key] = body.get(key)

    return payload

class GatewayHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _read_json(self):
        length = int(self.headers.get('Content-Length', 0))
        if length <= 0:
            self._last_raw_body = ''
            return {}
        raw = self.rfile.read(length).decode('utf-8')
        self._last_raw_body = raw
        return json.loads(raw)

    def do_GET(self):
        if self.path == "/control":
            self._send_json(fetch_control_status())
            return

        if self.path == "/control/status":
            self._send_json(fetch_control_status())
            return

        if self.path == "/health":
            conn = open_db()
            q = conn.execute("SELECT COUNT(*) FROM commands WHERE status='queued'").fetchone()[0]
            d = conn.execute("SELECT COUNT(*) FROM commands WHERE status='delivering'").fetchone()[0]
            conn.close()
            self._send_json({"ok": True, "service": "ai-bridge-local", "version": VERSION, "commands_queued": q, "commands_delivering": d, "timestamp": now_iso()})
            return

        if self.path.startswith("/bridge/pending-sources"):
            qs = parse_qs(urlparse(self.path).query)
            target_chat_id = qs.get("target_chat_id", ["gateway-brain-supervisor"])[0]

            conn = open_db()
            rows = conn.execute(
                "SELECT source_chat_id, COUNT(*) FROM commands WHERE status='queued' AND target_chat_id=? AND action='run-command' GROUP BY source_chat_id ORDER BY MIN(id) ASC",
                (target_chat_id,)
            ).fetchall()
            conn.close()

            sources = [
                {"source_chat_id": row[0], "queued": row[1]}
                for row in rows
                if row[0]
            ]
            self._send_json({"ok": True, "target_chat_id": target_chat_id, "sources": sources})
            return

        if self.path.startswith("/bridge/next-action"):
            fail_stale_deliveries()
            qs = parse_qs(urlparse(self.path).query)
            chat_id = qs.get("chat_id", ["gateway-brain-supervisor"])[0]
            source_chat_id = qs.get("source_chat_id", [""])[0]

            conn = open_db()
            if source_chat_id:
                row = conn.execute(
                    "SELECT * FROM commands WHERE status='queued' AND target_chat_id=? AND source_chat_id=? AND action='run-command' ORDER BY id ASC LIMIT 1",
                    (chat_id, source_chat_id)
                ).fetchone()
            else:
                row = conn.execute("SELECT * FROM commands WHERE status='queued' AND target_chat_id=? ORDER BY id ASC LIMIT 1", (chat_id,)).fetchone()
            if not row:
                conn.close()
                self._send_json({"ok": True, "action": None, "chat_id": chat_id})
                return

            cmd_id = row[1]
            conn.execute("UPDATE commands SET status='delivering', delivered_at=? WHERE command_id=?", (now_iso(), cmd_id))
            conn.commit()
            conn.close()

            payload = {}
            try:
                payload = json.loads(row[9]) if row[9] else {}
            except Exception:
                payload = {}

            self._send_json({
                "ok": True,
                "chat_id": chat_id,
                "action": {
                    "command_id": row[1],
                    "source_chat_id": row[2],
                    "target_chat_id": row[3],
                    "action": row[4],
                    "delivery_kind": row[5],
                    "conversation_id": row[6],
                    "from_agent": row[7],
                    "message": row[8],
                    "payload": payload
                }
            })
            return

        if self.path == '/event':
            event_type = body.get('event_type') or body.get('type')
            if not event_type:
                self._send_json(dict(ok=False, error='missing_event_type'), 400)
                return
            record_event(command_id=body.get('command_id'), event_type=event_type, message=body.get('message'), payload=body.get('payload') or {})
            self._send_json(dict(ok=True, event_type=event_type, timestamp=now_iso()))
            return

        self._send_json({"error": "not_found"}, 404)

    def do_POST(self):
        try:
            body = self._read_json()
        except Exception as e:
            record_invalid_message({}, 'invalid_json: ' + str(e), getattr(self, '_last_raw_body', ''))
            self._send_json({"ok": False, "error": "invalid_json", "detail": str(e)}, 400)
            return

        if self.path == "/bridge/commands":
            cmd_id = body.get("command_id", str(uuid.uuid4()))
            payload = normalize_payload(body)
            validation_error = validate_command_body(body, payload)
            if validation_error:
                record_invalid_message(body, validation_error)
                enqueue_source_feedback(body, 'invalid_envelope', validation_error)
                self._send_json(dict(ok=False, error='invalid_envelope', detail=validation_error), 400)
                return

            if body.get("action") == "run-command" and body.get("delivery_kind") == "local_capability":
                body["target_chat_id"] = "gateway-brain-supervisor"

            conn = open_db()
            try:
                conn.execute(
                    "INSERT INTO commands (command_id,source_chat_id,target_chat_id,action,delivery_kind,conversation_id,from_agent,message,payload_json) VALUES (?,?,?,?,?,?,?,?,?)",
                    (
                        cmd_id,
                        body.get("source_chat_id", ""),
                        body.get("target_chat_id", ""),
                        body.get("action", ""),
                        body.get("delivery_kind", ""),
                        body.get("conversation_id", ""),
                        body.get("from_agent", ""),
                        body.get("message", ""),
                        json.dumps(payload, ensure_ascii=False)
                    )
                )
                conn.commit()
                enqueue_source_feedback(body, 'accepted', 'queued')
                self._send_json({"ok": True, "command_id": cmd_id, "status": "queued", "target_chat_id": body.get("target_chat_id", "")})
            except sqlite3.IntegrityError:
                self._send_json({"ok": False, "error": "duplicate", "command_id": cmd_id}, 409)
            finally:
                conn.close()
            return

        if self.path == "/bridge/acks":
            conn = open_db()
            conn.execute(
                "UPDATE commands SET status=?,acked_at=?,return_code=?,stdout=?,stderr=?,last_error=? WHERE command_id=?",
                (
                    body.get("status", "acked"),
                    now_iso(),
                    body.get("return_code"),
                    body.get("stdout", ""),
                    body.get("stderr", ""),
                    body.get("error", ""),
                    body.get("command_id")
                )
            )
            if body.get('status') == 'failed':
                row = conn.execute('SELECT command_id, source_chat_id, target_chat_id, action, delivery_kind, payload_json FROM commands WHERE command_id=?', (body.get('command_id'),)).fetchone()
                if row:
                    conn.execute('INSERT INTO dead_letters (command_id, source_chat_id, target_chat_id, action, delivery_kind, payload_json, last_error, attempt_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', tuple(row) + (body.get('error', ''), 1))
            conn.commit()
            conn.close()
            self._send_json({"ok": True})
            return

        self._send_json({"error": "not_found"}, 404)

    def log_message(self, format, *args):
        pass

def main():
    print(f"[gateway] AI Bridge Local v{VERSION} - Porta {PORT} - Filtra por target_chat_id")
    init_db()
    ThreadingHTTPServer((HOST, PORT), GatewayHandler).serve_forever()

if __name__ == "__main__":
    main()

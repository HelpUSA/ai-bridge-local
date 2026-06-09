# -*- coding: utf-8 -*-
"""AI Bridge Local - Gateway HTTP v0.2.0 - Porta 8766 - Filtra por target_chat_id"""
import json, os, sqlite3, uuid
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

HOST = "127.0.0.1"
PORT = 8766
DB_PATH = os.path.join(os.path.dirname(__file__), "queue_local.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS commands (id INTEGER PRIMARY KEY AUTOINCREMENT, command_id TEXT UNIQUE NOT NULL, source_chat_id TEXT, target_chat_id TEXT, action TEXT, delivery_kind TEXT, conversation_id TEXT, from_agent TEXT, message TEXT, payload_json TEXT, status TEXT DEFAULT 'queued', created_at TEXT DEFAULT (datetime('now')), delivered_at TEXT, acked_at TEXT, return_code INTEGER, stdout TEXT, stderr TEXT, last_error TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, command_id TEXT, event_type TEXT, message TEXT, payload_json TEXT, created_at TEXT DEFAULT (datetime('now')))")
    conn.commit(); conn.close()

def now_iso(): return datetime.now(timezone.utc).isoformat()

class GatewayHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(body))); self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers(); self.wfile.write(body)
    def do_OPTIONS(self): self._send_json({})
    def do_GET(self):
        if self.path == "/health":
            conn = sqlite3.connect(DB_PATH)
            q = conn.execute("SELECT COUNT(*) FROM commands WHERE status='queued'").fetchone()[0]
            d = conn.execute("SELECT COUNT(*) FROM commands WHERE status='delivering'").fetchone()[0]
            conn.close()
            self._send_json({"ok":True,"service":"ai-bridge-local","version":"0.2.0","commands_queued":q,"commands_delivering":d,"timestamp":now_iso()})
        elif self.path.startswith("/bridge/next-action"):
            qs = parse_qs(urlparse(self.path).query)
            chat_id = qs.get("chat_id", ["gateway-brain-supervisor"])[0]
            conn = sqlite3.connect(DB_PATH)
            row = conn.execute("SELECT * FROM commands WHERE status='queued' AND target_chat_id=? ORDER BY id ASC LIMIT 1", (chat_id,)).fetchone()
            if not row: conn.close(); self._send_json({"ok":True,"action":None,"chat_id":chat_id}); return
            cmd_id = row[1]; conn.execute("UPDATE commands SET status='delivering', delivered_at=? WHERE command_id=?", (now_iso(), cmd_id)); conn.commit(); conn.close()
            self._send_json({"ok":True,"chat_id":chat_id,"action":{"command_id":row[1],"source_chat_id":row[2],"target_chat_id":row[3],"action":row[4],"delivery_kind":row[5],"conversation_id":row[6],"from_agent":row[7],"message":row[8],"payload":json.loads(row[9]) if row[9] else {}}})
        else: self._send_json({"error":"not_found"},404)
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length > 0 else {}
        if self.path == "/bridge/commands":
            cmd_id = body.get("command_id", str(uuid.uuid4()))
            conn = sqlite3.connect(DB_PATH)
            try:
                conn.execute("INSERT INTO commands (command_id,source_chat_id,target_chat_id,action,delivery_kind,conversation_id,from_agent,message,payload_json) VALUES (?,?,?,?,?,?,?,?,?)", (cmd_id, body.get("source_chat_id",""), body.get("target_chat_id",""), body.get("action",""), body.get("delivery_kind",""), body.get("conversation_id",""), body.get("from_agent",""), body.get("message",""), json.dumps(body.get("payload",{}))))
                conn.commit(); self._send_json({"ok":True,"command_id":cmd_id,"status":"queued","target_chat_id":body.get("target_chat_id","")})
            except sqlite3.IntegrityError: self._send_json({"ok":False,"error":"duplicate"},409)
            finally: conn.close()
        elif self.path == "/bridge/acks":
            conn = sqlite3.connect(DB_PATH)
            conn.execute("UPDATE commands SET status=?,acked_at=?,return_code=?,stdout=?,stderr=?,last_error=? WHERE command_id=?", (body.get("status","acked"), now_iso(), body.get("return_code"), body.get("stdout",""), body.get("stderr",""), body.get("error",""), body.get("command_id")))
            conn.commit(); conn.close(); self._send_json({"ok":True})
        else: self._send_json({"error":"not_found"},404)
    def log_message(self, format, *args): pass

def main():
    print("[gateway] AI Bridge Local v0.2.0 - Porta 8766 - Filtra por target_chat_id")
    init_db()
    HTTPServer((HOST, PORT), GatewayHandler).serve_forever()

if __name__ == "__main__": main()

from __future__ import annotations
import hashlib, json, os, random, re, secrets, sqlite3, subprocess, threading, time, traceback, uuid
from contextlib import closing
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse
VERSION="0.5.87"; ROOT=Path(__file__).resolve().parent
DB=Path(os.getenv("AI_BRIDGE_QUEUE_DB", str(ROOT/"queue_local.db"))).resolve()
HOST=os.getenv("AI_BRIDGE_COMMAND_HOST","127.0.0.1"); PORT=int(os.getenv("AI_BRIDGE_COMMAND_PORT","8767"))
MAX_INLINE=32768; MAX_BODY=1048576; MAX_RESULT=262144
class ProtocolError(ValueError): pass
class CapabilityError(RuntimeError): pass
def now(): return time.time()
def dump(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":"),default=str)
def summary(v,n=600):
    s=(v if isinstance(v,str) else dump(v)).replace("\r"," ").replace("\n"," ").strip()
    return s if len(s)<=n else s[:n-3]+"..."
def roots():
    raw=os.getenv("AI_BRIDGE_ALLOWED_ROOTS","").strip()
    return [Path(x).expanduser().resolve() for x in raw.split(";") if x.strip()] or [ROOT.resolve()]
def safe_path(value):
    p=Path(value); p=(p if p.is_absolute() else ROOT/p).expanduser().resolve()
    for root in roots():
        try: p.relative_to(root); return p
        except ValueError: pass
    raise CapabilityError("path outside allowed roots: "+str(p))
def normalize(x):
    if not isinstance(x,dict) or x.get("v",1)!=1: raise ProtocolError("invalid compact command")
    cid=str(x.get("id") or uuid.uuid4()).strip(); cap=str(x.get("cap") or "").strip(); args=x.get("args") or {}
    if not cid or len(cid)>160 or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,119}",cap): raise ProtocolError("invalid id or capability")
    if not isinstance(args,dict) or len(dump(args).encode())>MAX_INLINE: raise ProtocolError("args invalid or too large; use payload_ref")
    pref=x.get("payload_ref")
    if pref is not None and not re.fullmatch(r"sha256:[0-9a-f]{64}",str(pref)): raise ProtocolError("invalid payload_ref")
    raw_key=x.get("idempotency_key")
    key=None if raw_key is None or not str(raw_key).strip() else str(raw_key).strip()
    return {"id":cid,"cap":cap,"src":str(x.get("src") or ""),"dst":str(x.get("dst") or "gateway"),"args":args,"payload_ref":pref,"reply_mode":str(x.get("reply_mode") or "summary"),"max_attempts":min(max(int(x.get("max_attempts",5)),1),20),"key":key}
class Store:
    def __init__(self,db=None): self.db=Path(db or DB).resolve(); self.db.parent.mkdir(parents=True,exist_ok=True); self.schema()
    def con(self):
        c=sqlite3.connect(self.db,timeout=30,isolation_level=None); c.row_factory=sqlite3.Row
        c.execute("PRAGMA foreign_keys=ON"); c.execute("PRAGMA busy_timeout=30000"); c.execute("PRAGMA journal_mode=WAL"); return c
    def schema(self):
        sql="""
CREATE TABLE IF NOT EXISTS bridge2_payloads(payload_ref TEXT PRIMARY KEY,sha256 TEXT NOT NULL UNIQUE,content TEXT NOT NULL,encoding TEXT NOT NULL,size_bytes INTEGER NOT NULL,created_at REAL NOT NULL,expires_at REAL);
CREATE TABLE IF NOT EXISTS bridge2_commands(command_id TEXT PRIMARY KEY,idempotency_key TEXT UNIQUE,capability TEXT NOT NULL,source_chat_id TEXT,target_id TEXT,args_json TEXT NOT NULL,payload_ref TEXT,reply_mode TEXT NOT NULL,state TEXT NOT NULL,attempts INTEGER NOT NULL DEFAULT 0,max_attempts INTEGER NOT NULL,available_at REAL NOT NULL,lease_token TEXT,lease_expires_at REAL,last_error TEXT,result_id TEXT,created_at REAL NOT NULL,updated_at REAL NOT NULL,FOREIGN KEY(payload_ref) REFERENCES bridge2_payloads(payload_ref));
CREATE INDEX IF NOT EXISTS bridge2_claim ON bridge2_commands(state,available_at,lease_expires_at,created_at);
CREATE TABLE IF NOT EXISTS bridge2_results(result_id TEXT PRIMARY KEY,command_id TEXT NOT NULL UNIQUE,ok INTEGER NOT NULL,summary TEXT NOT NULL,data_json TEXT,created_at REAL NOT NULL,FOREIGN KEY(command_id) REFERENCES bridge2_commands(command_id));
CREATE TABLE IF NOT EXISTS bridge2_events(event_id INTEGER PRIMARY KEY AUTOINCREMENT,command_id TEXT,event_type TEXT NOT NULL,data_json TEXT,created_at REAL NOT NULL);
"""
        with closing(self.con()) as c:
            c.executescript(sql)
            columns={str(row[1]):int(row[3]) for row in c.execute("PRAGMA table_info(bridge2_commands)").fetchall()}
            notnull=columns.get("idempotency_key")
            if notnull==1:
                before=int(c.execute("SELECT COUNT(*) FROM bridge2_commands").fetchone()[0])
                c.execute("PRAGMA foreign_keys=OFF")
                try:
                    c.execute("BEGIN IMMEDIATE")
                    c.execute("DROP TABLE IF EXISTS bridge2_commands_nullable_0585")
                    c.execute("""
CREATE TABLE bridge2_commands_nullable_0585(
 command_id TEXT PRIMARY KEY,
 idempotency_key TEXT UNIQUE,
 capability TEXT NOT NULL,
 source_chat_id TEXT,
 target_id TEXT,
 args_json TEXT NOT NULL,
 payload_ref TEXT,
 reply_mode TEXT NOT NULL,
 state TEXT NOT NULL,
 attempts INTEGER NOT NULL DEFAULT 0,
 max_attempts INTEGER NOT NULL,
 available_at REAL NOT NULL,
 lease_token TEXT,
 lease_expires_at REAL,
 last_error TEXT,
 result_id TEXT,
 created_at REAL NOT NULL,
 updated_at REAL NOT NULL,
 FOREIGN KEY(payload_ref) REFERENCES bridge2_payloads(payload_ref)
)
""")
                    c.execute("""
INSERT INTO bridge2_commands_nullable_0585(
 command_id,idempotency_key,capability,source_chat_id,target_id,args_json,payload_ref,reply_mode,state,
 attempts,max_attempts,available_at,lease_token,lease_expires_at,last_error,result_id,created_at,updated_at
)
SELECT
 command_id,idempotency_key,capability,source_chat_id,target_id,args_json,payload_ref,reply_mode,state,
 attempts,max_attempts,available_at,lease_token,lease_expires_at,last_error,result_id,created_at,updated_at
FROM bridge2_commands
""")
                    copied=int(c.execute("SELECT COUNT(*) FROM bridge2_commands_nullable_0585").fetchone()[0])
                    if copied!=before: raise RuntimeError("bridge2 command count changed during nullable migration")
                    c.execute("DROP TABLE bridge2_commands")
                    c.execute("ALTER TABLE bridge2_commands_nullable_0585 RENAME TO bridge2_commands")
                    c.execute("CREATE INDEX IF NOT EXISTS bridge2_claim ON bridge2_commands(state,available_at,lease_expires_at,created_at)")
                    c.execute("COMMIT")
                except BaseException:
                    if c.in_transaction:c.execute("ROLLBACK")
                    raise
                finally:
                    c.execute("PRAGMA foreign_keys=ON")
            elif notnull!=0:
                raise RuntimeError("unexpected bridge2_commands.idempotency_key schema")
            violations=c.execute("PRAGMA foreign_key_check").fetchall()
            if violations: raise RuntimeError("foreign key violation after command schema initialization")
    def event(self,cid,event,data=None):
        with closing(self.con()) as c: c.execute("INSERT INTO bridge2_events(command_id,event_type,data_json,created_at) VALUES(?,?,?,?)",(cid,event,None if data is None else dump(data),now()))
    def put_payload(self,content,encoding="utf-8",ttl=86400):
        raw=content.encode(encoding); digest=hashlib.sha256(raw).hexdigest(); ref="sha256:"+digest; created=now(); expires=None if ttl is None else created+min(max(int(ttl),60),2592000)
        with closing(self.con()) as c: c.execute("INSERT INTO bridge2_payloads VALUES(?,?,?,?,?,?,?) ON CONFLICT(payload_ref) DO UPDATE SET expires_at=excluded.expires_at",(ref,digest,content,encoding,len(raw),created,expires))
        return {"payload_ref":ref,"sha256":digest,"size_bytes":len(raw),"expires_at":expires}
    def payload(self,ref):
        with closing(self.con()) as c: row=c.execute("SELECT * FROM bridge2_payloads WHERE payload_ref=?",(ref,)).fetchone()
        return None if row is None or (row["expires_at"] is not None and row["expires_at"]<now()) else dict(row)
    def submit(self,value):
        x=normalize(value)
        if x["payload_ref"] and self.payload(x["payload_ref"]) is None: raise ProtocolError("payload missing or expired")
        t=now()
        with closing(self.con()) as c:
            c.execute("BEGIN IMMEDIATE"); row=c.execute("SELECT * FROM bridge2_commands WHERE command_id=? OR (? IS NOT NULL AND idempotency_key=?) LIMIT 1",(x["id"],x["key"],x["key"])).fetchone()
            if row is not None: c.execute("COMMIT"); out=dict(row); out["duplicate"]=True; return out
            c.execute("INSERT INTO bridge2_commands VALUES(?,?,?,?,?,?,?,?, 'queued',0,?,?,NULL,NULL,NULL,NULL,?,?)",(x["id"],x["key"],x["cap"],x["src"],x["dst"],dump(x["args"]),x["payload_ref"],x["reply_mode"],x["max_attempts"],t,t,t)); c.execute("COMMIT")
        self.event(x["id"],"queued",{"cap":x["cap"]}); return {"command_id":x["id"],"state":"queued","duplicate":False}
    def get(self,cid):
        with closing(self.con()) as c:
            row=c.execute("SELECT * FROM bridge2_commands WHERE command_id=?",(cid,)).fetchone()
            if row is None:return None
            out=dict(row); out["args"]=json.loads(out.pop("args_json"))
            if out.get("result_id"):
                r=c.execute("SELECT * FROM bridge2_results WHERE result_id=?",(out["result_id"],)).fetchone(); out["result"]=None if r is None else dict(r)
            return out
    def result(self,rid):
        with closing(self.con()) as c: row=c.execute("SELECT * FROM bridge2_results WHERE result_id=?",(rid,)).fetchone()
        return None if row is None else dict(row)
    def stats(self):
        with closing(self.con()) as c: rows=c.execute("SELECT state,COUNT(*) n FROM bridge2_commands GROUP BY state").fetchall()
        states={r["state"]:r["n"] for r in rows}; return {"version":VERSION,"database":str(self.db),"states":states,"pending":sum(states.get(x,0) for x in ("queued","retry_wait","leased","running"))}
    def requeue(self):
        t=now()
        with closing(self.con()) as c: cur=c.execute("UPDATE bridge2_commands SET state='retry_wait',available_at=?,lease_token=NULL,lease_expires_at=NULL,last_error=COALESCE(last_error,'lease expired'),updated_at=? WHERE state IN('leased','running') AND lease_expires_at<?",(t,t,t))
        return cur.rowcount
    def claim(self,lease=60):
        t=now(); token=secrets.token_urlsafe(24); expires=t+max(int(lease),10)
        with closing(self.con()) as c:
            c.execute("BEGIN IMMEDIATE"); row=c.execute("SELECT * FROM bridge2_commands WHERE state IN('queued','retry_wait') AND available_at<=? AND (lease_expires_at IS NULL OR lease_expires_at<?) ORDER BY created_at LIMIT 1",(t,t)).fetchone()
            if row is None:c.execute("COMMIT");return None
            cur=c.execute("UPDATE bridge2_commands SET state='leased',lease_token=?,lease_expires_at=?,updated_at=? WHERE command_id=? AND state IN('queued','retry_wait')",(token,expires,t,row["command_id"]))
            if cur.rowcount!=1:c.execute("ROLLBACK");return None
            c.execute("COMMIT")
        out=dict(row); out["lease_token"]=token; out["args"]=json.loads(out.pop("args_json")); return out
    def running(self,cid,token):
        with closing(self.con()) as c: cur=c.execute("UPDATE bridge2_commands SET state='running',updated_at=? WHERE command_id=? AND lease_token=? AND state='leased'",(now(),cid,token))
        return cur.rowcount==1
    def complete(self,cid,token,data):
        rid=str(uuid.uuid4()); t=now(); raw=dump(data)
        if len(raw.encode())>MAX_RESULT:data={"truncated":True,"summary":summary(data,4000)};raw=dump(data)
        with closing(self.con()) as c:
            c.execute("BEGIN IMMEDIATE"); row=c.execute("SELECT 1 FROM bridge2_commands WHERE command_id=? AND lease_token=? AND state IN('leased','running')",(cid,token)).fetchone()
            if row is None:c.execute("ROLLBACK");raise RuntimeError("lease lost")
            c.execute("INSERT INTO bridge2_results VALUES(?,?,1,?,?,?)",(rid,cid,summary(data),raw,t)); c.execute("UPDATE bridge2_commands SET state='completed',result_id=?,lease_token=NULL,lease_expires_at=NULL,updated_at=? WHERE command_id=?",(rid,t,cid)); c.execute("COMMIT")
        return rid
    def fail(self,cid,token,error):
        t=now(); message=str(error)[-12000:]
        with closing(self.con()) as c:
            c.execute("BEGIN IMMEDIATE"); row=c.execute("SELECT attempts,max_attempts FROM bridge2_commands WHERE command_id=? AND lease_token=?",(cid,token)).fetchone()
            if row is None:c.execute("ROLLBACK");return "lease_lost"
            attempts=row["attempts"]+1; dead=attempts>=row["max_attempts"]; state="dead_letter" if dead else "retry_wait"; available=t if dead else t+min(300,2**min(attempts,8))+random.random()*2
            c.execute("UPDATE bridge2_commands SET state=?,attempts=?,available_at=?,lease_token=NULL,lease_expires_at=NULL,last_error=?,updated_at=? WHERE command_id=?",(state,attempts,available,message,t,cid)); c.execute("COMMIT")
        return state
    def dead(self,limit=100):
        with closing(self.con()) as c: return [dict(r) for r in c.execute("SELECT command_id,capability,attempts,max_attempts,last_error,updated_at FROM bridge2_commands WHERE state='dead_letter' ORDER BY updated_at DESC LIMIT ?",(min(max(int(limit),1),1000),)).fetchall()]
    def set_state(self,cid,state):
        t=now(); allowed="state IN('dead_letter','cancelled')" if state=="retry_wait" else "state NOT IN('completed','cancelled')"
        with closing(self.con()) as c: cur=c.execute(f"UPDATE bridge2_commands SET state=?,attempts=CASE WHEN ?='retry_wait' THEN 0 ELSE attempts END,available_at=?,lease_token=NULL,lease_expires_at=NULL,updated_at=? WHERE command_id=? AND {allowed}",(state,state,t,t,cid))
        return cur.rowcount==1
STORE=None; LOCK=threading.Lock(); API_STARTED=False; WORKER_STARTED=False; REG={}
def store():
    global STORE
    with LOCK:
        if STORE is None:STORE=Store()
    return STORE
def register(name,handler,read_only=True,confirm=False,description=""):REG[name]={"handler":handler,"read_only":read_only,"confirm":confirm,"description":description}
def cap_health(a,c):return {"ok":True,"version":VERSION,"pid":os.getpid(),"queue":store().stats()}
def cap_queue(a,c):return store().stats()
def cap_dead(a,c):return {"items":store().dead(a.get("limit",100))}
def cap_git(a,c):
    repo=safe_path(a.get("repo") or ROOT)
    def g(*x):
        p=subprocess.run(["git","-C",str(repo),*x],text=True,encoding="utf-8",errors="replace",stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=20)
        if p.returncode:raise CapabilityError(p.stdout.strip())
        return p.stdout.rstrip()
    return {"repo":str(repo),"branch":g("branch","--show-current"),"head":g("rev-parse","HEAD"),"status":g("status","--porcelain=v1","--untracked-files=all").splitlines()}
def cap_read(a,c):
    if not a.get("path"):raise CapabilityError("path required")
    p=safe_path(a.get("path")); raw=p.read_bytes(); limit=min(max(int(a.get("max_bytes",65536)),1),1048576); data=raw[:limit]
    return {"path":str(p),"size_bytes":len(raw),"truncated":len(data)<len(raw),"content":data.decode(a.get("encoding","utf-8"),errors="replace")}
def cap_run(a,c):
    if os.getenv("AI_BRIDGE_ENABLE_LOCAL_RUN","0")!="1":raise CapabilityError("local.run disabled")
    cmd=a.get("command");
    if not isinstance(cmd,list) or not cmd:raise CapabilityError("command must be array")
    cmd=[str(x) for x in cmd]; exe=Path(cmd[0]).name.lower()
    if exe not in {"python","python.exe","py","py.exe","git","git.exe","node","node.exe"}:raise CapabilityError("executable not allowed")
    p=subprocess.run(cmd,cwd=safe_path(a.get("cwd") or ROOT),text=True,encoding="utf-8",errors="replace",stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=min(max(int(a.get("timeout_seconds",60)),1),300),shell=False)
    return {"return_code":p.returncode,"output":p.stdout[:65536]}
register("runtime.health",cap_health,description="Command plane health")
register("queue.inspect",cap_queue,description="Queue counters")
register("queue.dead_letters",cap_dead,description="Dead letters")
register("git.inspect",cap_git,description="Git inspection")
register("file.read",cap_read,description="Read allowlisted file")
register("local.run",cap_run,read_only=False,confirm=True,description="Run allowlisted executable")
def execute(command):
    s=store(); cid=command["command_id"]; token=command["lease_token"]
    if not s.running(cid,token):return
    args=dict(command["args"]); pref=command.get("payload_ref")
    if pref:
        payload=s.payload(pref)
        if payload is None:s.fail(cid,token,"payload missing");return
        args["_payload"]=payload
    try:
        item=REG.get(command["capability"])
        if item is None:raise CapabilityError("unknown capability")
        if item["confirm"] and not args.get("confirmed"):raise CapabilityError("confirmed=true required")
        s.complete(cid,token,item["handler"](args,{"command_id":cid,"store":s}))
    except BaseException as e:s.fail(cid,token,e)
def worker_loop():
    s=store(); last=0.0
    while True:
        try:
            if now()-last>30:s.requeue();last=now()
            command=s.claim()
            if command is None:time.sleep(.5);continue
            execute(command)
        except BaseException:traceback.print_exc();time.sleep(2)
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*a):
        if os.getenv("AI_BRIDGE_COMMAND_HTTP_LOG","0")=="1":super().log_message(*a)
    def sendj(self,status,value):
        raw=dump(value).encode();self.send_response(status);self.send_header("Content-Type","application/json");self.send_header("Content-Length",str(len(raw)));self.send_header("Access-Control-Allow-Origin","*");self.send_header("Access-Control-Allow-Headers","Content-Type");self.send_header("Access-Control-Allow-Methods","GET,POST,OPTIONS");self.end_headers();self.wfile.write(raw)
    def body(self):
        length=int(self.headers.get("Content-Length","0") or 0)
        if length>MAX_BODY:raise ProtocolError("body too large")
        value=json.loads((self.rfile.read(length) if length else b"{}").decode())
        if not isinstance(value,dict):raise ProtocolError("body must be object")
        return value
    def do_OPTIONS(self):self.sendj(200,{"ok":True})
    def do_GET(self):
        try:
            path=urlparse(self.path).path.rstrip("/") or "/"; s=store()
            if path in {"/","/health"}:return self.sendj(200,{"ok":True,"service":"ai-bridge-command-plane","version":VERSION,"port":PORT,"queue":s.stats()})
            if path=="/v1/capabilities":return self.sendj(200,{"ok":True,"version":VERSION,"capabilities":[{"name":k,**{x:v for x,v in item.items() if x!="handler"}} for k,item in sorted(REG.items())]})
            if path=="/v1/queue/summary":return self.sendj(200,{"ok":True,"queue":s.stats()})
            if path=="/v1/queue/dead-letters":return self.sendj(200,{"ok":True,"items":s.dead()})
            if path.startswith("/v1/commands/"):
                command_id=unquote(path[len("/v1/commands/"):]).strip()
                if command_id and "/" not in command_id:
                    command=s.get(command_id)
                    if command is None:return self.sendj(404,{"ok":False,"error":"command_not_found","command_id":command_id})
                    return self.sendj(200,{"ok":True,"version":VERSION,"command":command})
                return self.sendj(404,{"ok":False,"error":"not_found"})
            if path.startswith("/v1/results/"):
                value=s.result(unquote(path[12:]));return self.sendj(200 if value else 404,{"ok":bool(value),"result":value})
            self.sendj(404,{"ok":False,"error":"not_found"})
        except BaseException as e:self.sendj(400 if isinstance(e,(ProtocolError,ValueError)) else 500,{"ok":False,"error":str(e)})
    def do_POST(self):
        try:
            path=urlparse(self.path).path.rstrip("/") or "/"; body=self.body();s=store()
            if path=="/v1/payloads":
                if not isinstance(body.get("content"),str):raise ProtocolError("content must be string")
                return self.sendj(201,{"ok":True,**s.put_payload(body["content"],body.get("encoding","utf-8"),body.get("ttl_seconds",86400))})
            if path=="/v1/commands/compact":return self.sendj(202,{"ok":True,"version":VERSION,**s.submit(body)})
            if path=="/v1/admin/requeue-expired":return self.sendj(200,{"ok":True,"requeued":s.requeue()})
            if path in {"/v1/admin/retry","/v1/admin/cancel"}:
                if not body.get("confirmed"):raise ProtocolError("confirmed=true required")
                state="retry_wait" if path.endswith("retry") else "cancelled";return self.sendj(200,{"ok":True,"changed":s.set_state(str(body.get("command_id") or ""),state)})
            self.sendj(404,{"ok":False,"error":"not_found"})
        except BaseException as e:self.sendj(400 if isinstance(e,(ProtocolError,ValueError)) else 500,{"ok":False,"error":str(e)})
def api_loop():ThreadingHTTPServer((HOST,PORT),Handler).serve_forever(.5)
def start_gateway_command_api(namespace=None):
    global API_STARTED
    with LOCK:
        if API_STARTED:return {"ok":True,"already_started":True,"version":VERSION}
        thread=threading.Thread(target=api_loop,name="ai-bridge-command-api",daemon=True);thread.start();API_STARTED=True
    return {"ok":True,"already_started":False,"version":VERSION,"port":PORT}
def start_compact_worker(namespace=None):
    global WORKER_STARTED
    with LOCK:
        if WORKER_STARTED:return {"ok":True,"already_started":True,"version":VERSION}
        thread=threading.Thread(target=worker_loop,name="ai-bridge-compact-worker",daemon=True);thread.start();WORKER_STARTED=True
    return {"ok":True,"already_started":False,"version":VERSION}

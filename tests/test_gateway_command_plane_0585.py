import sqlite3,sys,tempfile,time,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from gateway_command_plane import Store,normalize
class T(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.s=Store(Path(self.tmp.name)/"q.db")
 def tearDown(self):self.tmp.cleanup()
 def test_payload(self):self.assertEqual(self.s.put_payload("x")["payload_ref"],self.s.put_payload("x")["payload_ref"])
 def test_idempotency(self):
  a=self.s.submit({"id":"a","cap":"runtime.health","idempotency_key":"k"});b=self.s.submit({"id":"b","cap":"runtime.health","idempotency_key":"k"});self.assertFalse(a["duplicate"]);self.assertTrue(b["duplicate"])
 def test_complete(self):
  self.s.submit({"id":"c","cap":"runtime.health"});x=self.s.claim();self.assertTrue(self.s.running(x["command_id"],x["lease_token"]));self.s.complete(x["command_id"],x["lease_token"],{"ok":1});self.assertEqual(self.s.get("c")["state"],"completed")
 def test_expired(self):
  self.s.submit({"id":"e","cap":"runtime.health"});x=self.s.claim();c=self.s.con();c.execute("UPDATE bridge2_commands SET lease_expires_at=? WHERE command_id='e'",(time.time()-1,));c.close();self.assertEqual(self.s.requeue(),1)
 def test_large(self):
  with self.assertRaises(ValueError):normalize({"id":"x","cap":"file.read","args":{"x":"z"*40000}})
 def test_schema(self):
  c=sqlite3.connect(self.s.db);tables={r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")};c.close();self.assertIn("bridge2_commands",tables)
 def test_missing_or_blank_idempotency_key_does_not_dedupe(self):
  a=self.s.submit({"id":"blank-a","cap":"runtime.health"})
  b=self.s.submit({"id":"blank-b","cap":"runtime.health"})
  c=self.s.submit({"id":"blank-c","cap":"runtime.health","idempotency_key":"   "})
  d=self.s.submit({"id":"explicit-d","cap":"runtime.health","idempotency_key":" shared "})
  e=self.s.submit({"id":"explicit-e","cap":"runtime.health","idempotency_key":"shared"})
  repeat=self.s.submit({"id":"blank-a","cap":"runtime.health"})
  self.assertFalse(a["duplicate"]);self.assertFalse(b["duplicate"]);self.assertFalse(c["duplicate"])
  self.assertFalse(d["duplicate"]);self.assertTrue(e["duplicate"]);self.assertTrue(repeat["duplicate"])
  self.assertIsNone(self.s.get("blank-a")["idempotency_key"]);self.assertIsNone(self.s.get("blank-b")["idempotency_key"]);self.assertIsNone(self.s.get("blank-c")["idempotency_key"])
 def test_legacy_schema_migrates_idempotency_key_to_nullable(self):
  import sqlite3
  db=Path(self.tmp.name)/"legacy.db"
  c=sqlite3.connect(db)
  c.executescript('CREATE TABLE bridge2_payloads(payload_ref TEXT PRIMARY KEY,sha256 TEXT NOT NULL UNIQUE,content TEXT NOT NULL,encoding TEXT NOT NULL,size_bytes INTEGER NOT NULL,created_at REAL NOT NULL,expires_at REAL);CREATE TABLE bridge2_commands(command_id TEXT PRIMARY KEY,idempotency_key TEXT NOT NULL UNIQUE,capability TEXT NOT NULL,source_chat_id TEXT,target_id TEXT,args_json TEXT NOT NULL,payload_ref TEXT,reply_mode TEXT NOT NULL,state TEXT NOT NULL,attempts INTEGER NOT NULL DEFAULT 0,max_attempts INTEGER NOT NULL,available_at REAL NOT NULL,lease_token TEXT,lease_expires_at REAL,last_error TEXT,result_id TEXT,created_at REAL NOT NULL,updated_at REAL NOT NULL,FOREIGN KEY(payload_ref) REFERENCES bridge2_payloads(payload_ref));INSERT INTO bridge2_commands VALUES("legacy-command","legacy-key","runtime.health","","gateway","{}",NULL,"summary","queued",0,5,1,NULL,NULL,NULL,NULL,1,1);');c.close()
  legacy=Store(db)
  c=legacy.con()
  info={str(row[1]):int(row[3]) for row in c.execute("PRAGMA table_info(bridge2_commands)").fetchall()}
  self.assertEqual(info["idempotency_key"],0)
  self.assertEqual(c.execute("SELECT COUNT(*) FROM bridge2_commands").fetchone()[0],1)
  self.assertEqual(c.execute("SELECT command_id FROM bridge2_commands").fetchone()[0],"legacy-command")
  self.assertEqual(c.execute("PRAGMA integrity_check").fetchone()[0],"ok")
  self.assertEqual(c.execute("PRAGMA foreign_key_check").fetchall(),[])
  c.close()
if __name__=="__main__":unittest.main(verbosity=2)

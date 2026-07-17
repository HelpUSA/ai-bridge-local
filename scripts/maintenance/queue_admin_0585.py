import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from gateway_command_plane import Store
p=argparse.ArgumentParser();p.add_argument("--db",type=Path);s=p.add_subparsers(dest="action",required=True)
s.add_parser("summary");s.add_parser("requeue-expired");d=s.add_parser("dead-letters");d.add_argument("--limit",type=int,default=100)
for name in ("retry","cancel"):s.add_parser(name).add_argument("command_id")
a=p.parse_args();q=Store(a.db)
if a.action=="summary":out=q.stats()
elif a.action=="requeue-expired":out={"requeued":q.requeue(),"summary":q.stats()}
elif a.action=="dead-letters":out=q.dead(a.limit)
elif a.action=="retry":out={"changed":q.set_state(a.command_id,"retry_wait")}
else:out={"changed":q.set_state(a.command_id,"cancelled")}
print(json.dumps(out,ensure_ascii=False,indent=2,default=str))

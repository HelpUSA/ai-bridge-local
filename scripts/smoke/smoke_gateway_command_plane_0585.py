import json,time,urllib.request,uuid
BASE="http://127.0.0.1:8767"
def req(method,path,data=None):
 raw=None if data is None else json.dumps(data).encode();headers={"Accept":"application/json"}
 if raw is not None:headers["Content-Type"]="application/json"
 with urllib.request.urlopen(urllib.request.Request(BASE+path,data=raw,method=method,headers=headers),timeout=5) as r:return r.status,json.loads(r.read())
_,h=req("GET","/health");assert h["version"]=="0.5.87",h
_,caps=req("GET","/v1/capabilities");names={x["name"] for x in caps["capabilities"]};assert {"runtime.health","queue.inspect","git.inspect","file.read","local.run"}<=names
cid="smoke-"+str(uuid.uuid4());status,a=req("POST","/v1/commands/compact",{"v":1,"id":cid,"cap":"runtime.health","args":{}});assert status==202,a;assert a["command_id"]==cid,a
end=time.time()+30
while time.time()<end:
 _,x=req("GET","/v1/commands/"+cid);state=x["command"]["state"]
 if state in {"completed","dead_letter","cancelled"}:break
 time.sleep(.5)
assert state=="completed",x
print(json.dumps({"command_api_version":h["version"],"command_id":cid,"state":state,"FINAL_VERDICT":"READY"},indent=2))

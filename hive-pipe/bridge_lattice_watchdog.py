#!/usr/bin/env python3
"""Self-repairing hysteresis lattice for One-Wave bridge routes.

A single failed probe does not flap a route. Repeated failures cross a repair
threshold; repeated good probes are required before a repaired route is
promoted healthy again. State survives watchdog invocations.
"""
from __future__ import annotations
import argparse, json, os, pathlib, subprocess, time
from datetime import datetime, timezone

HERE=pathlib.Path(__file__).resolve().parent
STATE=pathlib.Path(os.environ.get("XDG_STATE_HOME", pathlib.Path.home()/".local/state"))/"one-wave-bridge-lattice"
STATE_FILE=STATE/"hysteresis.json"
RECEIPTS=STATE/"watchdog.jsonl"
FAIL_THRESHOLD=int(os.environ.get("BRIDGE_FAIL_THRESHOLD","3"))
RECOVER_THRESHOLD=int(os.environ.get("BRIDGE_RECOVER_THRESHOLD","2"))
COOLDOWN_SECONDS=int(os.environ.get("BRIDGE_REPAIR_COOLDOWN","60"))

SERVICES={
 "hive-pipe-agent.service":r"agent\.sh --watch",
 "hive-pipe-gateway.service":r"gateway\.py .*8765",
 "one-wave-chatgpt-terminal-pull.service":r"chatgpt_terminal_pull\.py --watch",
 "hive-pipe-relay.service":r"cloudflared tunnel .* run",
}
INSTALLERS={
 "hive-pipe-gateway.service":HERE/"install_gateway.sh",
 "hive-pipe-agent.service":HERE/"install_gateway.sh",
 "one-wave-chatgpt-terminal-pull.service":HERE/"install_chatgpt_terminal_pull.sh",
 "hive-pipe-relay.service":HERE/"install_persistent_relay.sh",
}
TRANSPORT={"hive-pipe-gateway.service","one-wave-chatgpt-terminal-pull.service"}
PUBLIC={"hive-pipe-relay.service","one-wave-chatgpt-terminal-pull.service"}

def run(argv,timeout=15):
 return subprocess.run(argv,text=True,capture_output=True,timeout=timeout,check=False)

def load_state():
 try:return json.loads(STATE_FILE.read_text())
 except (FileNotFoundError,json.JSONDecodeError):return {"services":{}}

def save_state(s):
 STATE.mkdir(parents=True,exist_ok=True)
 tmp=STATE_FILE.with_suffix(".tmp")
 tmp.write_text(json.dumps(s,sort_keys=True,indent=2)+"\n")
 os.replace(tmp,STATE_FILE)

def receipt(event):
 STATE.mkdir(parents=True,exist_ok=True)
 event={"at":datetime.now(timezone.utc).isoformat(),**event}
 with RECEIPTS.open("a",encoding="utf-8") as h:h.write(json.dumps(event,sort_keys=True)+"\n")
 print(json.dumps(event,sort_keys=True),flush=True)

def active(service,pattern):
 p=run(["systemctl","--user","is-active",service],8)
 if p.returncode==0 and p.stdout.strip()=="active":return True,"systemd-active"
 q=run(["pgrep","-af",pattern],8)
 return (q.returncode==0 and bool(q.stdout.strip())),("process-active" if q.returncode==0 and q.stdout.strip() else (p.stdout or p.stderr).strip() or "inactive")

def repair(service):
 p=run(["systemctl","--user","restart",service],20)
 ok,detail=active(service,SERVICES[service])
 if ok:return True,detail,(p.stderr or p.stdout).strip()[-1000:]
 msg=((p.stderr or "")+" "+(p.stdout or "")).lower()
 installer=INSTALLERS.get(service)
 if installer and installer.is_file() and ("not found" in msg or "not loaded" in msg or "could not be found" in msg):
  q=run(["/usr/bin/bash",str(installer)],60)
  ok,detail=active(service,SERVICES[service])
  return ok,detail,(q.stderr or q.stdout).strip()[-1000:]
 return False,detail,(p.stderr or p.stdout).strip()[-1000:]

def cycle():
 now=time.time(); persisted=load_state(); ps=persisted.setdefault("services",{}); view={}
 for service,pattern in SERVICES.items():
  raw,detail=active(service,pattern)
  s=ps.setdefault(service,{"fail":0,"good":0,"stable":False,"last_repair":0})
  if raw:
   s["fail"]=0;s["good"]=int(s.get("good",0))+1
   if s["good"]>=RECOVER_THRESHOLD:s["stable"]=True
  else:
   s["good"]=0;s["fail"]=int(s.get("fail",0))+1
   # Hysteresis: retain stable state until failure threshold is crossed.
   if s["fail"]>=FAIL_THRESHOLD:s["stable"]=False
  item={"raw_ok":raw,"detail":detail,"fail_count":s["fail"],"good_count":s["good"],"stable":s["stable"]}
  if not raw and s["fail"]>=FAIL_THRESHOLD and now-float(s.get("last_repair",0))>=COOLDOWN_SECONDS:
   s["last_repair"]=now
   ok,rdetail,msg=repair(service)
   item.update({"repair_attempted":True,"repair_ok":ok,"repair_detail":rdetail,"message":msg})
   if ok:
    # Do not promote immediately. Recovery must pass future probes.
    s["fail"]=0;s["good"]=1;s["stable"]=False
  view[service]=item
 stable={k for k,s in ps.items() if s.get("stable")}
 healthy=bool(stable&TRANSPORT) and bool(stable&PUBLIC) and len(stable)>=2
 persisted["updated_at"]=datetime.now(timezone.utc).isoformat()
 persisted["healthy"]=healthy
 save_state(persisted)
 receipt({"event":"bridge-hysteresis-cycle","healthy":healthy,"stable":sorted(stable),"thresholds":{"fail":FAIL_THRESHOLD,"recover":RECOVER_THRESHOLD,"cooldown_seconds":COOLDOWN_SECONDS},"services":view})
 return 0 if healthy else 1

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--watch",action="store_true");ap.add_argument("--interval",type=int,default=30);a=ap.parse_args()
 if not a.watch:raise SystemExit(cycle())
 while True:
  try:cycle()
  except Exception as e:receipt({"event":"watchdog-error","error":f"{type(e).__name__}: {e}"})
  time.sleep(max(10,a.interval))
if __name__=="__main__":main()

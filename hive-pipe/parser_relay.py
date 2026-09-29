#!/usr/bin/env python3
"""Two-state durable parser relay.

FIELD: inspect/validate a durable request and available route evidence.
VOID: hold/switch when the selected route cannot produce a matching receipt.
This controller never executes an unparsed arbitrary payload and never treats a
queued request as machine execution.
"""
from __future__ import annotations
import argparse,json,subprocess,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PARSER=HERE/"terminal_parser.py"
MAX_FAILURES=3

def run(a,timeout=30):
 return subprocess.run(a,text=True,capture_output=True,timeout=timeout,check=False)

def validate(req):
 required=("id","argv","intention","consequence")
 for k in required:
  if k not in req: raise ValueError(f"missing {k}")
 if not isinstance(req["id"],str) or not req["id"]: raise ValueError("invalid id")
 if not isinstance(req["argv"],list) or not req["argv"] or not all(isinstance(x,str) and x for x in req["argv"]): raise ValueError("invalid argv")
 return req

def route_state():
 probes=[]
 for name,cmd in [
  ("pull",["systemctl","--user","is-active","one-wave-chatgpt-terminal-pull.service"]),
  ("gateway",["systemctl","--user","is-active","hive-pipe-gateway.service"]),
  ("relay",["systemctl","--user","is-active","hive-pipe-relay.service"])]:
  p=run(cmd,8); probes.append({"route":name,"live":p.returncode==0 and p.stdout.strip()=="active","detail":(p.stdout or p.stderr).strip()})
 return probes

def cycle(request_path:Path,state_path:Path):
 req=validate(json.loads(request_path.read_text()))
 try: state=json.loads(state_path.read_text())
 except Exception: state={"schema":"one-wave-parser-relay-state/v1","requests":{}}
 ent=state["requests"].setdefault(req["id"],{"phase":"FIELD","failures":0,"attempts":[]})
 routes=route_state(); live=[x["route"] for x in routes if x["live"]]
 ent["routes"]=routes
 if live:
  ent["phase"]="FIELD"; ent["selected_route"]=live[0]
  ent["next_action"]="Dispatch only through the selected authenticated route; require matching final receipt."
 else:
  ent["failures"]+=1; ent["phase"]="VOID"
  ent["selected_route"]=None
  ent["next_action"]="HOLD durable request; retry on route return."
  if ent["failures"]>=MAX_FAILURES:
   ent["next_action"]="SWITCH ANGLE: bootstrap via an independent startup/host route; do not repeat dead transport."
 ent["attempts"].append({"at":time.time(),"phase":ent["phase"],"live_routes":live})
 state_path.parent.mkdir(parents=True,exist_ok=True)
 state_path.write_text(json.dumps(state,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"request_id":req["id"],"phase":ent["phase"],"live_routes":live,"failures":ent["failures"],"next_action":ent["next_action"]},sort_keys=True))
 return 0 if live else 2

if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("request");ap.add_argument("--state",default=str(Path.home()/".local/state/one-wave-parser-relay/state.json"));a=ap.parse_args()
 raise SystemExit(cycle(Path(a.request),Path(a.state)))

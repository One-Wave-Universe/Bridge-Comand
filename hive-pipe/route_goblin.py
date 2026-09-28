#!/usr/bin/env python3
"""Route Goblin: machine-first recovery parser for the One-Wave bridge.

This controller never treats the user as a transport. It classifies a failed
operation, tries executable local routes, and when none are live emits a
durable machine-readable recovery request for the Git transport/mailbox.

It cannot manufacture execution on a powered-off/unreachable host; instead it
makes that state durable so the first returning route resumes automatically.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
from typing import Any

HERE = Path(__file__).resolve().parent
STATE = Path(os.environ.get("XDG_STATE_HOME", Path.home()/".local/state"))/"one-wave-route-goblin"
STATE_FILE = STATE/"state.json"
OUTBOX = STATE/"recovery-outbox.jsonl"

@dataclass
class RouteProbe:
    name: str
    live: bool
    detail: str
    repair: list[str] | None = None

def run(argv:list[str], timeout:int=15)->subprocess.CompletedProcess[str]:
    return subprocess.run(argv,text=True,capture_output=True,timeout=timeout,check=False)

def now()->str:
    return datetime.now(timezone.utc).isoformat()

def probe_service(name:str, process_pattern:str, repair:list[str]|None=None)->RouteProbe:
    p=run(["systemctl","--user","is-active",name],8)
    if p.returncode==0 and p.stdout.strip()=="active":
        return RouteProbe(name,True,"systemd-active",repair)
    q=run(["pgrep","-af",process_pattern],8)
    if q.returncode==0 and q.stdout.strip():
        return RouteProbe(name,True,"process-active",repair)
    detail=(p.stdout or p.stderr or q.stderr or "inactive").strip()[-500:]
    return RouteProbe(name,False,detail,repair)

def routes()->list[RouteProbe]:
    return [
      probe_service("one-wave-chatgpt-terminal-pull.service",r"chatgpt_terminal_pull\.py --watch",
                    ["systemctl","--user","restart","one-wave-chatgpt-terminal-pull.service"]),
      probe_service("hive-pipe-gateway.service",r"gateway\.py .*8765",
                    ["systemctl","--user","restart","hive-pipe-gateway.service"]),
      probe_service("hive-pipe-relay.service",r"cloudflared tunnel .* run",
                    ["systemctl","--user","restart","hive-pipe-relay.service"]),
    ]

def append_outbox(event:dict[str,Any])->None:
    STATE.mkdir(parents=True,exist_ok=True)
    with OUTBOX.open("a",encoding="utf-8") as h:
        h.write(json.dumps(event,sort_keys=True)+"\n")

def save(obj:dict[str,Any])->None:
    STATE.mkdir(parents=True,exist_ok=True)
    tmp=STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    os.replace(tmp,STATE_FILE)

def cycle(repair:bool=True)->int:
    before=routes()
    attempts=[]
    if repair:
        # Repair every locally executable route. A failed repair is data, not a
        # reason to ask a human to become the bridge.
        for route in before:
            if route.live or not route.repair:
                continue
            p=run(route.repair,25)
            attempts.append({"route":route.name,"argv":route.repair,
                             "exit_code":p.returncode,
                             "stderr":p.stderr.strip()[-500:]})
    after=routes()
    live=[r.name for r in after if r.live]
    event={
      "at":now(),
      "event":"route-goblin-cycle",
      "state":"LIVE" if live else "DURABLE_WAIT",
      "live_routes":live,
      "routes":[asdict(r) for r in after],
      "repair_attempts":attempts,
      "human_transport_required":False,
    }
    if not live:
        event["next_action"]="Keep recovery request durable; retry automatically when any machine route returns."
        append_outbox({
          "at":event["at"],
          "kind":"bridge-recovery-required",
          "priority":"high",
          "reason":"no-local-execution-route",
          "requested_actions":[
            "start one-wave-chatgpt-terminal-pull.service",
            "run bridge_lattice_watchdog.py once",
          ],
          "human_transport_required":False,
        })
    save(event)
    print(json.dumps(event,sort_keys=True))
    return 0 if live else 2

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--probe-only",action="store_true")
    args=ap.parse_args()
    raise SystemExit(cycle(repair=not args.probe_only))

if __name__=="__main__":
    main()

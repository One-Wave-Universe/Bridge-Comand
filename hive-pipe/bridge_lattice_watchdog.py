#!/usr/bin/env python3
"""One-Wave bridge lattice watchdog.

Runs locally and independently of any remote control route. It only performs
bounded service recovery for known bridge listeners and writes JSONL receipts.
"""
from __future__ import annotations
import argparse, json, os, pathlib, subprocess, time
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).resolve().parent
STATE = pathlib.Path(os.environ.get("XDG_STATE_HOME", pathlib.Path.home()/".local/state"))/"one-wave-bridge-lattice"
RECEIPTS = STATE/"watchdog.jsonl"

SERVICES = {
    "hive-pipe-agent.service": r"agent\.sh --watch",
    "hive-pipe-gateway.service": r"gateway\.py .*8765",
    "one-wave-chatgpt-terminal-pull.service": r"chatgpt_terminal_pull\.py --watch",
    "desktop-commander-remote.service": r"desktop-commander.*remote",
    "hive-pipe-relay.service": r"cloudflared tunnel .* run",
}

INSTALLERS = {
    "hive-pipe-gateway.service": HERE/"install_gateway.sh",
    "hive-pipe-agent.service": HERE/"install_gateway.sh",
    "hive-pipe-relay.service": HERE/"install_persistent_relay.sh",
}

def run(argv, timeout=15):
    return subprocess.run(argv, text=True, capture_output=True, timeout=timeout, check=False)

def active(service, pattern):
    p=run(["systemctl","--user","is-active",service],8)
    if p.returncode==0 and p.stdout.strip()=="active":
        return True, "systemd-active"
    q=run(["pgrep","-af",pattern],8)
    return (q.returncode==0 and bool(q.stdout.strip())), ("process-active" if q.returncode==0 and q.stdout.strip() else (p.stdout or p.stderr).strip() or "inactive")

def receipt(event):
    STATE.mkdir(parents=True,exist_ok=True)
    event={"at":datetime.now(timezone.utc).isoformat(),**event}
    with RECEIPTS.open("a",encoding="utf-8") as f:
        f.write(json.dumps(event,sort_keys=True)+"\n")
    print(json.dumps(event,sort_keys=True),flush=True)

def restart(service):
    p=run(["systemctl","--user","restart",service],20)
    ok,detail=active(service,SERVICES[service])
    if ok:
        return ok, detail, (p.stderr or p.stdout).strip()[-1000:]
    # If a canonical unit is missing after repo migration, recreate it from the
    # checked-in installer. Installers are bounded and keep credentials local.
    installer=INSTALLERS.get(service)
    missing=("not found" in (p.stderr or "").lower() or "not loaded" in (p.stderr or "").lower())
    if installer and installer.is_file() and missing:
        q=run(["/usr/bin/bash",str(installer)],45)
        ok,detail=active(service,SERVICES[service])
        return ok, detail, (q.stderr or q.stdout).strip()[-1000:]
    return ok, detail, (p.stderr or p.stdout).strip()[-1000:]

def cycle():
    states={}
    for service,pattern in SERVICES.items():
        ok,detail=active(service,pattern)
        states[service]={"ok":ok,"detail":detail}
        if not ok:
            rok,rdetail,msg=restart(service)
            states[service].update({"repair_attempted":True,"repair_ok":rok,"repair_detail":rdetail,"message":msg})
    # Never declare the lattice healthy from one route. Healthy means at least
    # two independent local listeners are alive, including pull or gateway.
    alive=[k for k,v in states.items() if v.get("ok") or v.get("repair_ok")]
    transport=any(k in alive for k in ("one-wave-chatgpt-terminal-pull.service","hive-pipe-gateway.service"))
    public=any(k in alive for k in ("one-wave-chatgpt-terminal-pull.service","desktop-commander-remote.service","hive-pipe-relay.service"))
    healthy=len(alive)>=2 and transport and public
    receipt({"event":"bridge-lattice-cycle","healthy":healthy,"alive":alive,"services":states})
    return 0 if healthy else 1

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--watch",action="store_true")
    ap.add_argument("--interval",type=int,default=30)
    args=ap.parse_args()
    if not args.watch:
        raise SystemExit(cycle())
    while True:
        try: cycle()
        except Exception as e: receipt({"event":"watchdog-error","error":f"{type(e).__name__}: {e}"})
        time.sleep(max(10,args.interval))

if __name__=="__main__":
    main()

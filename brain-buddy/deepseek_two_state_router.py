#!/usr/bin/env python3
"""Two-state Brain Buddy route selector: OBSERVE <-> ACT.

Git/reference is authority. Routes are transports only. A failed route is observed,
recorded, and the next route is tried; no empty HOLD state is created.
"""
from __future__ import annotations
import argparse,json,os,subprocess,time,urllib.request
from pathlib import Path

def probe(url,timeout=2):
    try:
        with urllib.request.urlopen(url,timeout=timeout) as r:
            return r.status==200, r.read(512).decode(errors="replace")
    except Exception as e: return False,str(e)

def run(argv,timeout):
    try:
        p=subprocess.run(argv,text=True,capture_output=True,timeout=timeout)
        return p.returncode==0,(p.stdout or "")+(p.stderr or "")
    except Exception as e:return False,str(e)

def routes():
    science=os.environ.get("ONE_WAVE_SCIENCE","/home/Scales/One-Wave-Science")
    return [
      ("free-web-worker",["bash",f"{science}/scripts/deepseek_web_worker.sh"]),
      ("firefox-session",["python3",f"{science}/One_Wave_Bench/hive-pipe/deepseek_web_bridge.py"]),
      ("direct-model",["python3",f"{science}/One_Wave_Bench/hive-pipe/deepseek_bridge.py"]),
    ]

def main():
    ap=argparse.ArgumentParser();ap.add_argument("prompt");ap.add_argument("--timeout",type=int,default=120);ap.add_argument("--receipt",default="deepseek-route-receipt.json");a=ap.parse_args()
    receipt={"schema":"brain-buddy-two-state-router/v1","state":"OBSERVE","attempts":[],"answer":None}
    for name,cmd in routes():
        receipt["state"]="OBSERVE"
        # ACT only after selecting a concrete route; failures return to OBSERVE.
        receipt["state"]="ACT"; ok,out=run(cmd+[a.prompt],a.timeout)
        item={"route":name,"ok":ok,"output":out[-12000:]};receipt["attempts"].append(item)
        if ok and out.strip():
            receipt["answer"]=out.strip();receipt["selected_route"]=name;receipt["state"]="OBSERVE"
            Path(a.receipt).write_text(json.dumps(receipt,indent=2));print(out.strip());return 0
        receipt["state"]="OBSERVE"
    Path(a.receipt).write_text(json.dumps(receipt,indent=2))
    print(json.dumps(receipt,indent=2));return 1
if __name__=="__main__":raise SystemExit(main())

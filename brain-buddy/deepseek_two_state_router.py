#!/usr/bin/env python3
"""Adaptive DeepSeek transport worker. OBSERVE selects; ACT delegates; failures re-enter OBSERVE."""
from __future__ import annotations
import argparse,json,os,subprocess
from pathlib import Path

SCIENCE=os.environ.get("ONE_WAVE_SCIENCE","/home/Scales/One-Wave-Science")

def run(name,argv,prompt,timeout,env=None):
    e=os.environ.copy()
    if env:e.update(env)
    try:
        p=subprocess.run(argv+[prompt],text=True,capture_output=True,timeout=timeout,env=e)
        out=((p.stdout or "")+(p.stderr or "")).strip()
        return {"route":name,"ok":p.returncode==0 and bool(out),"output":out[-16000:]}
    except Exception as x:return {"route":name,"ok":False,"output":str(x)}

def routes():
    bridge=f"{SCIENCE}/One_Wave_Bench/hive-pipe/deepseek_web_bridge.py"
    return [
      ("selenium-session-3001",["python3",bridge,"--max-tool-rounds","12"],
       {"DEEPSEEK_WEB_BASE_URL":"http://127.0.0.1:3001","DEEPSEEK_WEB_API_KEY":"local-session"}),
      ("canonical-free-web",["bash",f"{SCIENCE}/scripts/deepseek_web_worker.sh"],{}),
      ("node-session-3000",["python3",bridge,"--max-tool-rounds","12"],
       {"DEEPSEEK_WEB_BASE_URL":"http://127.0.0.1:3000","DEEPSEEK_WEB_API_KEY":"usb-local"}),
    ]

def main():
    a=argparse.ArgumentParser();a.add_argument("prompt");a.add_argument("--timeout",type=int,default=120);a.add_argument("--receipt",default="deepseek-route-receipt.json");x=a.parse_args()
    rec={"schema":"brain-buddy-two-state-router/v2","state":"OBSERVE","attempts":[]}
    for name,argv,env in routes():
        rec["state"]="ACT"; item=run(name,argv,x.prompt,x.timeout,env);rec["attempts"].append(item);rec["state"]="OBSERVE"
        if item["ok"]:
            rec["selected_route"]=name;rec["answer"]=item["output"];Path(x.receipt).write_text(json.dumps(rec,indent=2));print(item["output"]);return 0
    rec["answer"]=None;Path(x.receipt).write_text(json.dumps(rec,indent=2));print(json.dumps(rec,indent=2));return 1
if __name__=="__main__":raise SystemExit(main())

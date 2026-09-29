#!/usr/bin/env python3
"""Independent GitHub-backed live machine executor.
Dedicated transport, separate state, bounded terminal_parser execution.
"""
from __future__ import annotations
import argparse,json,subprocess,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
STATE=Path.home()/".local/state/one-wave-live-executor"
BRANCH="machine-executor"
REQ=".machine-executor/request.json"
RES=".machine-executor/result.json"

def sh(*a,check=False):
 return subprocess.run(a,text=True,capture_output=True,check=check)

def git(*a):
 return sh("git",*a)

def read_branch(path):
 p=git("show",f"transport/{BRANCH}:{path}")
 if p.returncode: raise RuntimeError(p.stderr.strip())
 return json.loads(p.stdout)

def publish(runtime,result):
 git("-C",str(runtime),"checkout","-B","machine-executor-runtime",f"transport/{BRANCH}")
 (runtime/".machine-executor").mkdir(exist_ok=True)
 (runtime/RES).write_text(json.dumps(result,indent=2)+"\n")
 git("-C",str(runtime),"add",RES)
 git("-C",str(runtime),"commit","-m",f"machine receipt: {result['id']}")
 p=git("-C",str(runtime),"push","transport","HEAD:"+BRANCH)
 if p.returncode: raise RuntimeError(p.stderr.strip())

def execute(runtime):
 git("-C",str(runtime),"fetch","transport",BRANCH)
 req=read_branch(REQ)
 STATE.mkdir(parents=True,exist_ok=True)
 seen=STATE/"last-id"
 if seen.exists() and seen.read_text().strip()==req.get("id"): return False
 argv=req.get("argv"); rid=req.get("id")
 if not isinstance(rid,str) or not rid or not isinstance(argv,list) or not argv:
  raise ValueError("invalid request")
 # terminal_parser remains execution authority.
 import sys
 sys.path.insert(0,str(HERE))
 import terminal_parser
 result=terminal_parser.run(argv,cwd=req.get("cwd"),timeout=req.get("timeout",120))
 receipt={"schema":"one-wave-machine-executor-receipt/v1","id":rid,"ok":result.get("ok",False),
          "exit_code":result.get("exit_code"),"stdout":result.get("stdout",""),
          "stderr":result.get("stderr",""),"cwd":result.get("cwd"),"parser_contract":result.get("parser_contract")}
 publish(runtime,receipt); seen.write_text(rid+"\n"); return True

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--runtime",required=True);ap.add_argument("--watch",action="store_true");a=ap.parse_args()
 runtime=Path(a.runtime)
 while True:
  try: execute(runtime)
  except Exception as e: print("LIVE_EXECUTOR_HOLD",type(e).__name__,e,flush=True)
  if not a.watch:return 0
  time.sleep(10)
if __name__=="__main__":raise SystemExit(main())

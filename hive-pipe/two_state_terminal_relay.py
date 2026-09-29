#!/usr/bin/env python3
"""Two-state terminal relay. FIELD executes; VOID returns stdout/stderr."""
from __future__ import annotations
import argparse,json,subprocess,time,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; STATE=Path.home()/".local/state/one-wave-two-state-relay"
BRANCH="machine-executor"; REQ=".machine-executor/request.json"; RES=".machine-executor/response.json"
def sh(*a): return subprocess.run(a,text=True,capture_output=True)
def git(r,*a): return sh("git","-C",str(r),*a)
def load(r):
 p=git(r,"fetch","transport",BRANCH)
 if p.returncode: raise RuntimeError(p.stderr.strip())
 p=git(r,"show",f"transport/{BRANCH}:{REQ}")
 if p.returncode: raise RuntimeError(p.stderr.strip())
 return json.loads(p.stdout)
def relay(r,m):
 p=git(r,"checkout","-B","two-state-relay-runtime",f"transport/{BRANCH}")
 if p.returncode: raise RuntimeError(p.stderr.strip())
 o=r/RES; o.parent.mkdir(exist_ok=True); o.write_text(json.dumps(m,indent=2)+"\n")
 git(r,"add",RES)
 p=git(r,"-c","user.name=One-Wave Jetson","-c","user.email=jetson@localhost","commit","-m",f"relay response: {m['id']}")
 if p.returncode: raise RuntimeError(p.stderr.strip())
 p=git(r,"push","transport","HEAD:"+BRANCH)
 if p.returncode: raise RuntimeError(p.stderr.strip())
def cycle(r):
 q=load(r); rid=q.get("id"); argv=q.get("argv"); STATE.mkdir(parents=True,exist_ok=True); seen=STATE/"last-id"
 if not isinstance(rid,str) or not rid or not isinstance(argv,list) or not argv: raise ValueError("invalid request")
 if seen.exists() and seen.read_text().strip()==rid:return False
 sys.path.insert(0,str(HERE)); import terminal_parser
 try:
  x=terminal_parser.run(argv,cwd=q.get("cwd"),timeout=q.get("timeout",120))
  m={"schema":"one-wave-two-state-relay/v1","id":rid,"state":"VOID","ok":bool(x.get("ok")),"exit_code":x.get("exit_code"),"stdout":x.get("stdout",""),"stderr":x.get("stderr",""),"guidance":x.get("guidance",{})}
 except Exception as e:m={"schema":"one-wave-two-state-relay/v1","id":rid,"state":"VOID","ok":False,"exit_code":None,"stdout":"","stderr":f"{type(e).__name__}: {e}"}
 relay(r,m);seen.write_text(rid+"\n");return True
def main():
 a=argparse.ArgumentParser();a.add_argument("--runtime",required=True);a.add_argument("--watch",action="store_true");z=a.parse_args();r=Path(z.runtime)
 while True:
  try:cycle(r)
  except Exception as e:print("TWO_STATE_RELAY_HOLD",type(e).__name__,e,flush=True)
  if not z.watch:return 0
  time.sleep(5)
if __name__=="__main__":raise SystemExit(main())

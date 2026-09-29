#!/usr/bin/env python3
"""Non-destructive Bridge-Comand recovery/health doctor."""
from __future__ import annotations
import argparse, json, os, shutil, socket, subprocess, sys, time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
QUEUE=ROOT/"queue"
DIRS=("pending","processing","results","done","failed")
REQUIRED=("mudl.py","agent.sh","gateway.py","terminal_parser.py")

def check(name, ok, detail):
    print(("PASS" if ok else "FAIL").ljust(5), name.ljust(28), detail)
    return ok

def recover_stale(seconds:int):
    p=QUEUE/"processing"; q=QUEUE/"pending"; q.mkdir(parents=True,exist_ok=True)
    now=time.time(); moved=[]
    if not p.exists(): return moved
    for f in p.glob("*.json"):
        result=QUEUE/"results"/f.name; done=QUEUE/"done"/f.name
        if result.exists() or done.exists(): continue
        if now-f.stat().st_mtime >= seconds:
            target=q/f.name
            if not target.exists():
                os.replace(f,target); moved.append(f.name)
    return moved

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repair",action="store_true",help="create queue dirs and recover stale leased jobs")
    ap.add_argument("--probe",action="store_true",help="run safe local end-to-end health job")
    ap.add_argument("--stale-seconds",type=int,default=300)
    a=ap.parse_args()
    ok=True
    if a.repair:
        for d in DIRS:(QUEUE/d).mkdir(parents=True,exist_ok=True)
        for n in recover_stale(a.stale_seconds): print("RECOVERED",n)
    ok &= check("python",sys.version_info>=(3,10),sys.version.split()[0])
    ok &= check("git",shutil.which("git") is not None,shutil.which("git") or "missing")
    for f in REQUIRED: ok &= check(f,(ROOT/f).is_file(),str(ROOT/f))
    for d in DIRS:
        path=QUEUE/d
        ok &= check("queue/"+d,path.is_dir(),str(path))
    try:
        subprocess.run([sys.executable,"-m","py_compile",str(ROOT/"mudl.py"),str(ROOT/"gateway.py"),str(ROOT/"terminal_parser.py")],check=True,capture_output=True,text=True)
        ok &= check("python syntax",True,"bridge entry points compile")
    except Exception as e: ok &= check("python syntax",False,str(e))
    if a.probe and ok:
        try:
            en=subprocess.run([sys.executable,str(ROOT/"mudl.py"),"enqueue","health"],check=True,capture_output=True,text=True)
            req=Path(en.stdout.strip())
            run=subprocess.run([sys.executable,str(ROOT/"mudl.py"),"run",str(req)],check=True,capture_output=True,text=True)
            result=Path(run.stdout.strip())
            data=json.loads(result.read_text())
            ok &= check("end-to-end probe",data.get("exit_code")==0,f"receipt={result.name}")
        except Exception as e: ok &= check("end-to-end probe",False,str(e))
    print("BRIDGE_DOCTOR_EXIT="+("0" if ok else "2"))
    return 0 if ok else 2
if __name__=="__main__": raise SystemExit(main())

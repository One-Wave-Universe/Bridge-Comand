#!/usr/bin/env python3
"""Brain Buddy executable reference gate.

The worker process cannot start until BOTH conversation and repository
references are present and the repository checkout matches the packet.
"""
from __future__ import annotations
import argparse, hashlib, json, os, pathlib, subprocess, sys, time

BLOCK=64

def stop(reason):
    print(json.dumps({"brain_buddy": True, "gate": "BLOCKED", "reason": reason}), file=sys.stderr)
    raise SystemExit(BLOCK)

def need(obj,key,where):
    val=obj.get(key)
    if val is None or val=="" or val==[] or val=={}: stop(f"missing {where}.{key}")
    return val

def verify(packet, root):
    if packet.get("brain_buddy") is not True: stop("brain_buddy must be true")
    rid=need(packet,"request_id","packet"); need(packet,"question","packet")
    conv=need(packet,"conversation","packet")
    if not (conv.get("current_turns") or conv.get("prior_turns") or conv.get("turns")):
        stop("conversation has no actual turns or retrievable pointers")
    need(conv,"provenance","conversation")
    repo=need(packet,"repository","packet")
    need(repo,"owning_repo","repository"); branch=need(repo,"branch","repository")
    revision=need(repo,"revision","repository"); refs=need(repo,"relevant_references","repository")
    root=pathlib.Path(root).resolve()
    if not (root/".git").exists(): stop("repository checkout unavailable")
    try:
        head=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
        active=subprocess.check_output(["git","-C",str(root),"branch","--show-current"],text=True).strip()
    except Exception as e: stop("cannot verify git checkout: "+str(e))
    if head != revision: stop(f"stale/wrong revision: packet={revision} checkout={head}")
    if active and active != branch: stop(f"wrong branch: packet={branch} checkout={active}")
    paths=[]
    canonical=repo.get("canonical_start")
    if canonical: paths.append(canonical)
    for x in refs:
        p=x.get("path") if isinstance(x,dict) else x
        if p and p not in paths: paths.append(p)
    verified=[]
    for p in paths:
        f=(root/p).resolve()
        if f!=root and root not in f.parents: stop("reference escapes repo: "+p)
        if not f.is_file(): stop("missing repo reference: "+p)
        b=f.read_bytes(); verified.append({"path":p,"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b)})
    out=dict(packet)
    out["gate"]={"status":"OPEN","request_id":rid,"verified_at":int(time.time()),"repo_branch":active,"repo_head":head,"references":verified}
    raw=json.dumps(out,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    out["gate"]["reference_packet_sha256"]=hashlib.sha256(raw).hexdigest()
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--packet",required=True); ap.add_argument("--repo-root",required=True)
    ap.add_argument("--emit"); ap.add_argument("worker",nargs=argparse.REMAINDER)
    a=ap.parse_args()
    try: packet=json.loads(pathlib.Path(a.packet).read_text(encoding="utf-8"))
    except Exception as e: stop("packet unreadable: "+str(e))
    gated=verify(packet,a.repo_root)
    payload=json.dumps(gated,ensure_ascii=False,indent=2)+"\n"
    if a.emit: pathlib.Path(a.emit).write_text(payload,encoding="utf-8")
    cmd=a.worker[1:] if a.worker and a.worker[0]=="--" else a.worker
    if not cmd:
        sys.stdout.write(payload); return 0
    env=os.environ.copy(); env["BRAIN_BUDDY_GATE"]="OPEN"; env["BRAIN_BUDDY_REQUEST_ID"]=gated["request_id"]
    # Worker is created ONLY after verify() succeeds.
    return subprocess.run(cmd,input=payload,text=True,env=env).returncode

if __name__=="__main__": raise SystemExit(main())

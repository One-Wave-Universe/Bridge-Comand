#!/usr/bin/env python3
"""Brain Buddy live app: Reference -> Build -> Check, continuously.

Workers keep independent transports. Gemini and DeepSeek are not collapsed.
Every returned worker result is a VIEW; only a matching returned receipt is PASS.
"""
from __future__ import annotations
import argparse, json, os, subprocess, uuid
from datetime import datetime, timezone
from pathlib import Path

SCHEMA="one-wave-brain-buddy-live/v1"
REFS=["GENERAL_REFERENCE_RULES.md","AI_CANONICAL_START_HERE.md",
      "Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md"]

def ts(): return datetime.now(timezone.utc).isoformat()
def repo():
    p=subprocess.run(["git","rev-parse","--show-toplevel"],text=True,capture_output=True)
    if p.returncode: raise SystemExit("Run inside Bridge-Comand")
    return Path(p.stdout.strip()).resolve()
def sp(root,sid): return root/"External_Work"/"brain_buddy"/"sessions"/(sid+".json")
def save(root,s):
    p=sp(root,s["session_id"]); p.parent.mkdir(parents=True,exist_ok=True)
    s["updated_at"]=ts(); p.write_text(json.dumps(s,indent=2)+"\n")
def load(root,sid): return json.loads(sp(root,sid).read_text())

def new(question,sid=None):
    return {"schema":SCHEMA,"session_id":sid or "bb-"+uuid.uuid4().hex[:12],
      "created_at":ts(),"updated_at":ts(),"question":question,"phase":"REFERENCE",
      "weight_of_time":{"unresolved":[],"useful_state_changes":0},
      "reference":{"files":REFS,"baseline_zero":"living; re-question after every check"},
      "views":[],"checks":[],"pending":[]}

def prompt(s,worker):
    views="\n\n".join(f'{v["worker"]}: {v["answer"]}' for v in s["views"][-8:]) or "(none)"
    return f"""BRAIN BUDDY LIVE — {s["phase"]}
Session {s["session_id"]}

Architecture: REFERENCE -> BUILD -> CHECK -> REFERENCE.
This is a continuing asynchronous back-and-forth, not an answer pipeline.
Always reference. Question everything, including the current reference.
A worker response is a VIEW, never automatic truth or evidence.
Do not collapse providers, transports, failures, provenance, or state.
Agreement alone adds no weight. Preserve contradictions and HOLD when unresolved.
Only actual execution/evidence receipts can establish that something ran.

Reference chain:
{chr(10).join(REFS)}

Question/task:
{s["question"]}

Admitted views:
{views}

You are {worker}, one independent worker. Challenge the current state and advance the current
Reference/Build/Check pass. State what you referenced, what concrete build/test is next, and
what observable check would count. End with NEXT QUESTION: <strongest unresolved question>."""

def command(worker,p):
    env=os.environ.copy()
    if worker=="gemini":
        # Existing Gemini adapter owns its auth/secret behavior.
        return ["python3","brain_buddy/hive_pipe/gemini_web_bridge.py","--max-tool-rounds","12",p],env
    if worker=="deepseek":
        # Logged-in DeepSeek web-session relay. Never substitute the hosted DeepSeek API.
        env.setdefault("DEEPSEEK_WEB_BASE_URL","http://192.168.55.100:3000")
        return ["python3","brain_buddy/hive_pipe/deepseek_web_bridge.py","--max-tool-rounds","12",p],env
    raise ValueError(worker)

def run(root,s,worker):
    rid=f'{s["session_id"]}-{len(s["views"])+1}-{worker}'
    cmd,env=command(worker,prompt(s,worker))
    p=subprocess.run(cmd,cwd=root,text=True,capture_output=True,env=env)
    return {"request_id":rid,"worker":worker,"transport":worker+"_adapter",
      "ok":p.returncode==0,"exit_code":p.returncode,"answer":p.stdout.strip(),
      "stderr":p.stderr.strip(),"returned_at":ts(),"reference_phase":s["phase"]}

def admit(s,v):
    s["views"].append(v)
    check={"request_id":v["request_id"],"matched_return":True,"ok":v["ok"],
           "checked_at":ts(),"rule":"returned receipt required; dispatch alone never PASS"}
    s["checks"].append(check)
    if v["ok"]: s["weight_of_time"]["useful_state_changes"]+=1
    else: s["weight_of_time"]["unresolved"].append(
        {"request_id":v["request_id"],"worker":v["worker"],"failure":v["stderr"] or "worker failed"})
    # Every CHECK returns to REFERENCE. The next worker sees the newly admitted state.
    s["phase"]="REFERENCE"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("question",nargs="?"); ap.add_argument("--session")
    ap.add_argument("--cycles",type=int,default=1)
    ap.add_argument("--worker",choices=["both","gemini","deepseek"],default="both")
    a=ap.parse_args(); r=repo()
    if a.session and sp(r,a.session).exists(): s=load(r,a.session)
    else:
        q=(a.question or "").strip() or input("Question/task: ").strip()
        if not q: raise SystemExit("Question required")
        s=new(q,a.session); save(r,s)
    workers=["gemini","deepseek"] if a.worker=="both" else [a.worker]
    for _ in range(max(1,a.cycles)):
        for w in workers:
            s["phase"]="BUILD"; save(r,s)
            v=run(r,s,w); admit(s,v); save(r,s)
            print("\n===== "+w.upper()+" / "+v["request_id"]+" =====")
            print(v["answer"] if v["ok"] else "HOLD — "+(v["stderr"] or str(v["exit_code"])))
    print("\nSESSION "+s["session_id"])
    print("STATE "+str(sp(r,s["session_id"]).relative_to(r)))
if __name__=="__main__": main()

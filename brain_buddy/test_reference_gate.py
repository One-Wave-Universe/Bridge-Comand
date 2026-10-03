#!/usr/bin/env python3
"""Tests that missing conversation blocks worker creation and valid refs open gate."""
import json,pathlib,subprocess,tempfile
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parent
GATE=HERE/"reference_gate.py"
head=subprocess.check_output(["git","-C",str(ROOT),"rev-parse","HEAD"],text=True).strip()
branch=subprocess.check_output(["git","-C",str(ROOT),"branch","--show-current"],text=True).strip()
def packet():
 return {"brain_buddy":True,"request_id":"reference-gate-selftest","question":"What is current?","conversation":{"current_turns":[{"speaker":"user","text":"Use conversation and repo."}],"provenance":{"source":"selftest"}},"repository":{"owning_repo":"One-Wave-Universe/Bridge-Comand","canonical_start":"BRIDGE_COMMAND_START_HERE.md","branch":branch,"revision":head,"relevant_references":["BRIDGE_COMMAND_START_HERE.md"]}}
with tempfile.TemporaryDirectory() as td:
 p=pathlib.Path(td)/"packet.json"; marker=pathlib.Path(td)/"worker_started"
 good=packet(); p.write_text(json.dumps(good))
 worker=["python3","-c",f"import pathlib,sys; pathlib.Path({str(marker)!r}).write_text(sys.stdin.read())"]
 ok=subprocess.run(["python3",str(GATE),"--packet",str(p),"--repo-root",str(ROOT),"--",*worker],capture_output=True,text=True)
 assert ok.returncode==0,(ok.returncode,ok.stderr)
 assert marker.exists(),"valid gate did not launch worker"
 marker.unlink()
 bad=packet(); bad["conversation"]={"provenance":{"source":"selftest"}}; p.write_text(json.dumps(bad))
 no=subprocess.run(["python3",str(GATE),"--packet",str(p),"--repo-root",str(ROOT),"--",*worker],capture_output=True,text=True)
 assert no.returncode==64,(no.returncode,no.stderr)
 assert not marker.exists(),"BLOCKED gate still launched worker"
 stale=packet(); stale["repository"]["revision"]="0"*40; p.write_text(json.dumps(stale))
 no=subprocess.run(["python3",str(GATE),"--packet",str(p),"--repo-root",str(ROOT),"--",*worker],capture_output=True,text=True)
 assert no.returncode==64,(no.returncode,no.stderr)
 assert not marker.exists(),"stale repo gate still launched worker"
print("REFERENCE_GATE_SELFTEST_PASS")

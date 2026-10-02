#!/usr/bin/env python3
"""Jetson Brain Buddy peer watcher: watches Git requests and delegates them to DeepSeek routes."""
import json,subprocess,time,urllib.request
from pathlib import Path
BRANCH="feature/git-centered-brain-buddy-20261003"
API="https://api.github.com/repos/One-Wave-Universe/Bridge-Comand/contents/.brain-buddy-dispatch?ref="+BRANCH
ROOT=Path.home()/".local/state/brain-buddy"; ROOT.mkdir(parents=True,exist_ok=True)
SEEN=ROOT/"deepseek-seen.txt"; OUT=ROOT/"deepseek-latest.json"
ROUTER=Path.home()/".local/share/brain-buddy/deepseek_two_state_router.py"
def get(url):
    with urllib.request.urlopen(url,timeout=20) as r:return json.load(r)
def once():
    items=get(API); reqs=[x for x in items if x.get("name","").startswith("request-") and x["name"].endswith(".json")]
    if not reqs:return
    x=sorted(reqs,key=lambda q:q["name"])[-1]
    if SEEN.exists() and SEEN.read_text().strip()==x["sha"]:return
    req=get(x["download_url"]); q=req["question"]; refs=", ".join(req.get("references",[]))
    prompt=("BRAIN BUDDY PEER. Original shared question: "+q+" Start from canonical Git. "
            "Inspect these references as needed: "+refs+". Independently reason; return supported conclusion, "
            "strongest objection, falsification condition, and next smallest test.")
    p=subprocess.run(["python3",str(ROUTER),"--timeout","120","--receipt",str(ROOT/"deepseek-route.json"),prompt],
                     text=True,capture_output=True,timeout=390)
    OUT.write_text(json.dumps({"request":req["id"],"request_sha":x["sha"],"ok":p.returncode==0,
                               "view":p.stdout[-20000:],"stderr":p.stderr[-4000:]},indent=2))
    SEEN.write_text(x["sha"])
if __name__=="__main__":
    while True:
        try: once()
        except Exception as e:(ROOT/"watcher-error.txt").write_text(str(e))
        time.sleep(30)

#!/usr/bin/env python3
import hashlib,json,os,pathlib,sys,urllib.request,urllib.error
def load(p): return json.loads(pathlib.Path(p).read_text())
def sha(b): return hashlib.sha256(b).hexdigest()
def evidence(req,root,out):
    r=load(req); base=pathlib.Path(root); refs=["AI_CANONICAL_START_HERE.md"]+r.get("references",[])
    files=[]
    for p in dict.fromkeys(refs):
        f=base/p
        if not f.is_file(): files.append({"path":p,"missing":True}); continue
        b=f.read_bytes(); files.append({"path":p,"sha256":sha(b),"text":b.decode(errors="replace")[:50000]})
    obj={"schema":"one-wave-shared-git-evidence/v1","request_id":r["id"],"science_head":os.popen(f"git -C {root} rev-parse HEAD").read().strip(),"files":files,"question":r["question"]}
    pathlib.Path(out).write_text(json.dumps(obj,indent=2))
def prompt(r,e,peer):
    return ("You are "+peer+" in a Git-centered Brain Buddy loop. Git/reference is the center, not a bridge. "
    "Use the exact shared evidence below. A worker never fills time with empty HOLD: it references, observes prior visible views, acts, or returns a view. "
    "Separate established evidence from One-Wave hypothesis. Do not invent measurements. State conclusion, strongest objection, falsification condition, and next exploration.\n\n"
    "QUESTION:\n"+r["question"]+"\n\nVISIBLE VIEWS:\n"+json.dumps(r.get("visible_views",[]))+"\n\nSHARED GIT EVIDENCE:\n"+json.dumps(e))
def post(url,payload,headers):
    q=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={"Content-Type":"application/json",**headers},method="POST")
    with urllib.request.urlopen(q,timeout=180) as x:return json.load(x)
def gemini(req,ev,out):
    r,e=load(req),load(ev); key=os.environ["GEMINI_API_KEY"]; model=r.get("gemini_model","gemini-3.5-flash")
    z=post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",{"contents":[{"role":"user","parts":[{"text":prompt(r,e,"Gemini")}]}]},{"x-goog-api-key":key})
    ans="\n".join(p["text"] for c in z.get("candidates",[]) for p in c.get("content",{}).get("parts",[]) if "text" in p)
    pathlib.Path(out).write_text(json.dumps({"actor":"GEMINI","status":"COMPLETE" if ans else "FAILED","answer":ans,"model":model},indent=2))
def deepseek(req,ev,out):
    r,e=load(req),load(ev); key=os.environ["DEEPSEEK_API_KEY"]; model=r.get("deepseek_model","deepseek-chat")
    z=post("https://api.deepseek.com/chat/completions",{"model":model,"messages":[{"role":"user","content":prompt(r,e,"DeepSeek")}],"temperature":0.2},{"Authorization":"Bearer "+key})
    ans=z["choices"][0]["message"]["content"]
    pathlib.Path(out).write_text(json.dumps({"actor":"DEEPSEEK","status":"COMPLETE","answer":ans,"model":z.get("model",model),"response_id":z.get("id")},indent=2))
def state(req,ev,out):
    r,e=load(req),load(ev); views=[]
    for p in ("gemini-view.json","deepseek-view.json"):
        if pathlib.Path(p).exists(): views.append(load(p))
    pathlib.Path(out).write_text(json.dumps({"schema":"one-wave-brain-buddy-state/v1","request_id":r["id"],"science_head":e["science_head"],"views":views,"next":"re-reference Git with returned views"},indent=2))
if __name__=="__main__":
    m=sys.argv[1]
    {"evidence":evidence,"gemini":gemini,"deepseek":deepseek,"state":state}[m](*sys.argv[2:])

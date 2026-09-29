#!/usr/bin/env python3
"""One-Wave phone AI relay parser/worker.

Two transport states only:
REQUEST -> RESPONSE

The worker does not control an AI app. It parses a small durable envelope,
preserves request/reference identity, and emits a handoff that Android can
share to the target AI. A returned AI message is parsed into a matching receipt.
"""
import argparse, hashlib, json, pathlib, sys, time

SCHEMA="one-wave-phone-ai-relay/v1"

def load(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))

def dump(obj,p=None):
    s=json.dumps(obj,indent=2,ensure_ascii=False)+"\n"
    if p: pathlib.Path(p).write_text(s,encoding="utf-8")
    else: sys.stdout.write(s)

def validate_request(x):
    need=("id","source","target","question","references")
    miss=[k for k in need if not x.get(k)]
    if miss: raise SystemExit("HOLD missing: "+",".join(miss))
    if x["source"]==x["target"]: raise SystemExit("HOLD source == target")
    return x

def handoff(x):
    validate_request(x)
    refs="\n".join(f"- {r}" for r in x["references"])
    body=(f"ONE-WAVE RELAY {SCHEMA}\nREQUEST_ID: {x['id']}\n"
          f"SOURCE: {x['source']}\nTARGET: {x['target']}\n"
          f"REFERENCES (inspect before answering):\n{refs}\n\n"
          f"QUESTION:\n{x['question']}\n\n"
          "RETURN RULE: Start your reply with exactly "
          f"REQUEST_ID: {x['id']} then give your answer.")
    return {"schema":SCHEMA,"state":"REQUEST","id":x["id"],
            "target":x["target"],"share_text":body,
            "references":x["references"]}

def receipt(req,response):
    validate_request(req)
    marker=f"REQUEST_ID: {req['id']}"
    if marker not in response:
        raise SystemExit("HOLD response does not match request ID")
    return {"schema":SCHEMA,"state":"RESPONSE","id":req["id"],
            "source":req["target"],"target":req["source"],
            "references":req["references"],"response":response,
            "response_sha256":hashlib.sha256(response.encode()).hexdigest(),
            "received_unix":int(time.time()),"ok":True}

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("handoff"); a.add_argument("request"); a.add_argument("-o","--out")
    b=sub.add_parser("receipt"); b.add_argument("request"); b.add_argument("response"); b.add_argument("-o","--out")
    ns=ap.parse_args()
    if ns.cmd=="handoff": dump(handoff(load(ns.request)),ns.out)
    else: dump(receipt(load(ns.request),pathlib.Path(ns.response).read_text(encoding="utf-8")),ns.out)
if __name__=="__main__": main()

#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, pathlib, subprocess
from urllib.request import Request, urlopen

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SCIENCE = pathlib.Path(os.environ.get("ONE_WAVE_SCIENCE_ROOT", "/home/Scales/One-Wave-Science"))
MCP_URL = os.environ.get("HIVE_PIPE_MCP_URL", "http://127.0.0.1:8765/mcp")
MARKER = "BRIDGE_DOCTOR_GATEWAY_OK"

def run(argv, cwd=None, timeout=20):
    return subprocess.run(argv, cwd=cwd or ROOT, text=True, capture_output=True, timeout=timeout, check=False)

def row(name, status, detail, action=""):
    print(f"{status:14} {name:32} {detail}")
    return {"name":name,"status":status,"detail":detail,"action":action}

def service_or_process(name, pattern):
    p = run(["systemctl","--user","is-active",name], timeout=8)
    state=(p.stdout or p.stderr).strip()
    if p.returncode==0 and p.stdout.strip()=="active":
        return row("service "+name,"PASS","active")
    q = run(["pgrep","-af",pattern], timeout=8)
    if q.returncode==0 and q.stdout.strip():
        return row("service "+name,"PASS","process active; user-systemd bus unavailable in this session")
    return row("service "+name,"FAIL",state or "inactive",f"Repair {name} and rerun this doctor.")

def token():
    direct=os.environ.get("HIVE_PIPE_TOKEN","").strip()
    if direct: return direct
    td=pathlib.Path.home()/".config/hive-pipe/tokens"
    preferred=td/"codex.token"
    paths=[preferred] if preferred.is_file() else sorted(td.glob("*.token")) if td.is_dir() else []
    return paths[0].read_text().strip() if paths else None

def mcp_call(tok,name,args):
    payload={"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":name,"arguments":args}}
    req=Request(MCP_URL,data=json.dumps(payload).encode(),headers={"Authorization":"Bearer "+tok,"Content-Type":"application/json"},method="POST")
    with urlopen(req,timeout=35) as r: env=json.load(r)
    if "error" in env: raise RuntimeError(env["error"])
    result=env.get("result",{}).get("structuredContent")
    if not isinstance(result,dict): raise RuntimeError("missing structuredContent")
    return result

def static_checks():
    out=[]
    required=["gateway.py","terminal_parser.py","install_gateway.sh","agent.sh","mudl.py",
              "create_client_token.sh","chatgpt_terminal_pull.py","install_chatgpt_terminal_pull.sh",
              "bootstrap_chatgpt_terminal_pull.sh","deepseek_bridge.py","deepseek_web_bridge.py"]
    missing=[x for x in required if not (HERE/x).is_file()]
    out.append(row("bridge files","PASS" if not missing else "FAIL",
                   "core bridge files present" if not missing else "missing: "+", ".join(missing)))
    py=[str(HERE/x) for x in required if x.endswith(".py")]
    p=run(["python3","-m","py_compile",*py])
    out.append(row("python syntax","PASS" if p.returncode==0 else "FAIL","ok" if p.returncode==0 else p.stderr[-1000:]))
    sh=[str(HERE/x) for x in required if x.endswith(".sh")]
    p=run(["bash","-n",*sh])
    out.append(row("shell syntax","PASS" if p.returncode==0 else "FAIL","ok" if p.returncode==0 else p.stderr[-1000:]))
    return out

def gateway_checks():
    out=[
        service_or_process("hive-pipe-agent.service",r"agent\.sh --watch"),
        service_or_process("hive-pipe-gateway.service",r"gateway\.py --host 127\.0\.0\.1 --port 8765"),
    ]
    tok=token()
    if not tok:
        out.append(row("local Hive Pipe MCP","FAIL","no local client token found"))
        return out
    try:
        ref=mcp_call(tok,"terminal_reference",{})
        smoke=mcp_call(tok,"terminal_run",{
            "argv":["printf",MARKER],"timeout":30,
            "intention":"Verify the local Hive Pipe route",
            "consequence":"Expect the marker and exit zero without changing repository state"
        })
        ok=smoke.get("stdout")==MARKER and smoke.get("exit_code")==0
        out.append(row("local Hive Pipe MCP","PASS" if ok else "FAIL",
                       f"receipt stdout={smoke.get('stdout')!r} exit={smoke.get('exit_code')}"))
    except Exception as e:
        out.append(row("local Hive Pipe MCP","FAIL",f"{type(e).__name__}: {e}"))
    return out

def pull_checks():
    if not SCIENCE.is_dir():
        return [row("pull bridge","WARN",f"science checkout not visible: {SCIENCE}")]
    p=run(["git","ls-remote","--heads","origin","chatgpt-terminal","chatgpt-terminal-backup"],cwd=SCIENCE)
    names={line.split("refs/heads/")[-1] for line in p.stdout.splitlines() if "refs/heads/" in line}
    ok={"chatgpt-terminal","chatgpt-terminal-backup"} <= names
    return [row("pull bridge","PASS" if ok else "FAIL",
                "primary and backup branches reachable" if ok else (p.stderr.strip() or str(sorted(names))))]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--profile",choices=["ci","gateway","pull","all"],default="all")
    ap.add_argument("--json",action="store_true")
    args=ap.parse_args()
    checks=static_checks()
    if args.profile in ("gateway","all"): checks += gateway_checks()
    if args.profile in ("pull","all"): checks += pull_checks()
    fail=any(x["status"]=="FAIL" for x in checks)
    warn=any(x["status"]=="WARN" for x in checks)
    code=1 if fail else (2 if warn else 0)
    if args.json: print(json.dumps({"profile":args.profile,"exit_code":code,"checks":checks},indent=2))
    else: print(f"\nBRIDGE_DOCTOR_EXIT={code}")
    raise SystemExit(code)

if __name__=="__main__": main()

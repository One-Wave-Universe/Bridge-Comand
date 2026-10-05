#!/usr/bin/env python3
"""Signed Jetson-to-laptop terminal relay; no private credentials in requests."""
import argparse, base64, hashlib, json, os, socket, sqlite3, subprocess
import tempfile, time, urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

CONFIG = Path.home() / ".config/one-wave-laptop-relay"
STATE = Path.home() / ".local/state/one-wave-laptop-relay"
MAX_BODY = 65536

def crypto(operation, key, data, signature=None):
    with tempfile.TemporaryDirectory() as folder:
        p = Path(folder)
        (p / "data").write_bytes(data)
        argv = ["openssl", "pkeyutl", "-rawin", "-in", str(p / "data")]
        if operation == "sign":
            argv += ["-sign", "-inkey", str(key)]
        else:
            (p / "signature").write_bytes(signature)
            argv += ["-verify", "-pubin", "-inkey", str(key), "-sigfile", str(p / "signature")]
        x = subprocess.run(argv, capture_output=True, timeout=10)
        if x.returncode:
            raise ValueError("signature operation failed")
        return x.stdout

def envelope(data, private_key):
    raw = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    return json.dumps({"payload": base64.b64encode(raw).decode(),
                       "signature": base64.b64encode(crypto("sign", private_key, raw)).decode()}).encode()

def unwrap(raw, public_key):
    x = json.loads(raw)
    data = base64.b64decode(x["payload"], validate=True)
    sig = base64.b64decode(x["signature"], validate=True)
    crypto("verify", public_key, data, sig)
    return json.loads(data), hashlib.sha256(data).hexdigest()

def request_digest(q):
    action = {k: v for k, v in q.items() if k != "issued_at"}
    return hashlib.sha256(json.dumps(action, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def handle(raw):
    q, _ = unwrap(raw, CONFIG / "peer-public.pem")
    digest = request_digest(q)
    rid = q.get("id")
    if not isinstance(rid, str) or not 1 <= len(rid) <= 128:
        raise ValueError("invalid request id")
    if abs(time.time() - float(q["issued_at"])) > 120:
        raise ValueError("request expired")
    if q.get("target") != socket.gethostname():
        raise ValueError("target identity mismatch")
    if not q.get("intention") or not q.get("consequence"):
        raise ValueError("intention and consequence required")
    STATE.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(STATE / "receipts.sqlite") as db:
        db.execute("CREATE TABLE IF NOT EXISTS receipts (id TEXT PRIMARY KEY, digest TEXT, result TEXT)")
        old = db.execute("SELECT digest,result FROM receipts WHERE id=?", (rid,)).fetchone()
        if old:
            if old[0] != digest:
                raise ValueError("request id reused with different content")
            if old[1] is None:
                raise ValueError("prior execution unresolved; reconcile before retry")
            return json.loads(old[1])
        db.execute("INSERT INTO receipts VALUES (?,?,NULL)", (rid, digest))
    import terminal_parser
    try:
        result = terminal_parser.run(q["argv"], cwd=q.get("cwd"), timeout=q.get("timeout", 30))
    except Exception as exc:
        result = {"ok": False, "exit_code": None, "stdout": "", "stderr": str(exc)}
    result.update({"schema": "one-wave-signed-laptop-receipt/v1", "id": rid,
                   "request_sha256": digest, "target": socket.gethostname(),
                   "user": os.environ.get("USER", ""), "returned_at": time.time(),
                   "intention": q["intention"], "consequence": q["consequence"]})
    with sqlite3.connect(STATE / "receipts.sqlite") as db:
        db.execute("UPDATE receipts SET result=? WHERE id=?", (json.dumps(result), rid))
    return result

class Handler(BaseHTTPRequestHandler):
    def setup(self):
        super().setup()
        self.connection.settimeout(10)
    def log_message(self, *args):
        pass
    def do_POST(self):
        if self.path != "/run":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= MAX_BODY:
                raise ValueError("invalid body size")
            result = handle(self.rfile.read(length))
            body = envelope(result, CONFIG / "private.pem")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except Exception:
            self.send_error(400, "Rejected request; inspect authentication, target, freshness, or request id")

def client(args):
    config = json.loads((CONFIG / "route.json").read_text())
    q = json.loads(args.request_json)
    q.setdefault("issued_at", time.time())
    q.setdefault("target", config["target"])
    raw = envelope(q, CONFIG / "private.pem")
    req = urllib.request.Request(config["url"].rstrip("/") + "/run", data=raw,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=min(300, int(q.get("timeout", 30))) + 15) as r:
        result, _ = unwrap(r.read(2 * 1024 * 1024), CONFIG / "peer-public.pem")
    digest = request_digest(q)
    if result.get("id") != q.get("id") or result.get("request_sha256") != digest or result.get("target") != q["target"]:
        raise ValueError("return does not match issued request")
    print(json.dumps(result, indent=2))
    return 0 if result.get("ok") and result.get("exit_code") == 0 else 1

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="mode", required=True)
    s = sub.add_parser("serve")
    s.add_argument("--bind", required=True)
    s.add_argument("--port", type=int, default=8766)
    c = sub.add_parser("client")
    c.add_argument("--request-json", required=True)
    args = p.parse_args()
    if args.mode == "client":
        return client(args)
    HTTPServer((args.bind, args.port), Handler).serve_forever()

if __name__ == "__main__":
    raise SystemExit(main())

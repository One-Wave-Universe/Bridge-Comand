#!/usr/bin/env python3
import importlib.util,json,tempfile
from pathlib import Path
p=Path(__file__).with_name("live_machine_executor.py")
spec=importlib.util.spec_from_file_location("live_machine_executor",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert m.BRANCH=="machine-executor"
assert m.REQ==".machine-executor/request.json"
assert m.RES==".machine-executor/result.json"
src=p.read_text()
for term in ("terminal_parser","one-wave-machine-executor-receipt/v1","--watch","time.sleep(10)"): assert term in src,term
installer=Path(__file__).with_name("install_live_machine_executor.sh").read_text()
for term in ("one-wave-live-machine-executor.service","Restart=always","WantedBy=default.target","enable --now"): assert term in installer,term
assert "sudo " not in installer
print("LIVE_MACHINE_EXECUTOR_CONTRACT_OK")

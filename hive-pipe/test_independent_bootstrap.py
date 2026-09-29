#!/usr/bin/env python3
from pathlib import Path
root=Path(__file__).parent
i=(root/"install_independent_bootstrap.sh").read_text()
s=(root/"run_bootstrap_supervisor.sh").read_text()
for x in ["one-wave-bootstrap.service","one-wave-bootstrap.timer","OnBootSec=10s","Persistent=true","enable --now one-wave-bootstrap.timer"]: assert x in i,x
for x in ["one-wave-chatgpt-terminal-pull.service","hive-pipe-gateway.service","bootstrap_chatgpt_terminal_pull.sh","one-wave-bootstrap-receipt/v1","phase=VOID","phase=FIELD"]: assert x in s,x
assert "sudo " not in i+s
print("INDEPENDENT_BOOTSTRAP_CONTRACT_OK")

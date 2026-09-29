#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
UNIT_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
mkdir -p "$UNIT_DIR"
cat >"$UNIT_DIR/one-wave-route-goblin.service" <<EOF
[Unit]
Description=One-Wave machine-first route recovery parser
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 $HERE/route_goblin.py
SuccessExitStatus=2
EOF
cat >"$UNIT_DIR/one-wave-route-goblin.timer" <<'EOF'
[Unit]
Description=Retry One-Wave bridge routes without human transport

[Timer]
OnBootSec=20
OnUnitActiveSec=30
Persistent=true

[Install]
WantedBy=timers.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now one-wave-route-goblin.timer
systemctl --user start one-wave-route-goblin.service || true
systemctl --user is-active one-wave-route-goblin.timer

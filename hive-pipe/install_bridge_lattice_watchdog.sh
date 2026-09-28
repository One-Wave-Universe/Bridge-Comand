#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
SYSTEMD_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
mkdir -p "$SYSTEMD_DIR"
cat >"$SYSTEMD_DIR/one-wave-bridge-lattice-watchdog.service" <<EOF
[Unit]
Description=One-Wave Bridge Lattice Watchdog
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=0

[Service]
Type=simple
ExecStart=/usr/bin/python3 $SCRIPT_DIR/bridge_lattice_watchdog.py --watch --interval 30
Restart=always
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now one-wave-bridge-lattice-watchdog.service
systemctl --user is-active one-wave-bridge-lattice-watchdog.service
echo BRIDGE_LATTICE_WATCHDOG_INSTALLED

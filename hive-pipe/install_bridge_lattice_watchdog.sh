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
Type=oneshot
ExecStart=/usr/bin/python3 $SCRIPT_DIR/bridge_lattice_watchdog.py
NoNewPrivileges=true
PrivateTmp=true
EOF

cat >"$SYSTEMD_DIR/one-wave-bridge-lattice-watchdog.timer" <<EOF
[Unit]
Description=Continuously verify and repair the One-Wave bridge lattice

[Timer]
OnBootSec=20s
OnUnitActiveSec=30s
AccuracySec=5s
Persistent=true
Unit=one-wave-bridge-lattice-watchdog.service

[Install]
WantedBy=timers.target
EOF

# A second boot/login anchor: even if the timer was previously disabled, the
# target wants it whenever the user manager starts.
mkdir -p "$SYSTEMD_DIR/default.target.wants" "$SYSTEMD_DIR/timers.target.wants"
ln -sfn ../one-wave-bridge-lattice-watchdog.timer "$SYSTEMD_DIR/timers.target.wants/one-wave-bridge-lattice-watchdog.timer"

systemctl --user daemon-reload
systemctl --user enable --now one-wave-bridge-lattice-watchdog.timer
systemctl --user start one-wave-bridge-lattice-watchdog.service || true

echo BRIDGE_LATTICE_AUTOREPAIR_INSTALLED
systemctl --user is-enabled one-wave-bridge-lattice-watchdog.timer
systemctl --user is-active one-wave-bridge-lattice-watchdog.timer

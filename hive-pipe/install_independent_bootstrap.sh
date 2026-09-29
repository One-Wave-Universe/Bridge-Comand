#!/usr/bin/env bash
set -euo pipefail
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
ROOT="$(CDPATH= cd -- "$HERE/.." && pwd)"
UNIT_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/one-wave-bootstrap"
PROJECT="${ONE_WAVE_PROJECT_ROOT:-/home/Scales/One-Wave-Science}"
mkdir -p "$UNIT_DIR" "$STATE_DIR"

cat >"$UNIT_DIR/one-wave-bootstrap.service" <<EOF
[Unit]
Description=One-Wave independent bridge bootstrap
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=0

[Service]
Type=oneshot
Environment=ONE_WAVE_PROJECT_ROOT=$PROJECT
ExecStart=/usr/bin/bash $HERE/run_bootstrap_supervisor.sh
NoNewPrivileges=true
PrivateTmp=true
TimeoutStartSec=180
EOF

cat >"$UNIT_DIR/one-wave-bootstrap.timer" <<'EOF'
[Unit]
Description=Ensure One-Wave bridge control plane can recover itself

[Timer]
OnBootSec=10s
OnUnitActiveSec=60s
AccuracySec=5s
Persistent=true
Unit=one-wave-bootstrap.service

[Install]
WantedBy=timers.target
EOF

mkdir -p "$UNIT_DIR/timers.target.wants" "$UNIT_DIR/default.target.wants"
ln -sfn ../one-wave-bootstrap.timer "$UNIT_DIR/timers.target.wants/one-wave-bootstrap.timer"
systemctl --user daemon-reload
systemctl --user enable --now one-wave-bootstrap.timer
systemctl --user start one-wave-bootstrap.service || true
echo ONE_WAVE_BOOTSTRAP_INSTALLED
systemctl --user is-enabled one-wave-bootstrap.timer
systemctl --user is-active one-wave-bootstrap.timer

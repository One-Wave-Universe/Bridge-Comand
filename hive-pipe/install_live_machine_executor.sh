#!/usr/bin/env bash
set -euo pipefail
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
ROOT="$(CDPATH= cd -- "$HERE/.." && pwd)"
PROJECT="${ONE_WAVE_PROJECT_ROOT:-/home/Scales/One-Wave-Science}"
TRANSPORT_URL="${ONE_WAVE_TRANSPORT_URL:-https://github.com/One-Wave-Universe/One-Wave-Science.git}"
RUNTIME="${XDG_DATA_HOME:-$HOME/.local/share}/one-wave-live-executor"
UNIT_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
mkdir -p "$(dirname "$RUNTIME")" "$UNIT_DIR"
if [[ ! -d "$RUNTIME/.git" ]]; then git clone --no-checkout "$TRANSPORT_URL" "$RUNTIME"; fi
git -C "$RUNTIME" remote set-url origin "$TRANSPORT_URL"
if git -C "$RUNTIME" remote get-url transport >/dev/null 2>&1; then git -C "$RUNTIME" remote set-url transport "$TRANSPORT_URL"; else git -C "$RUNTIME" remote add transport "$TRANSPORT_URL"; fi
git -C "$RUNTIME" fetch transport machine-executor
cat >"$UNIT_DIR/one-wave-live-machine-executor.service" <<EOF
[Unit]
Description=One-Wave two-state terminal relay
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=0
[Service]
Type=simple
WorkingDirectory=$RUNTIME
ExecStart=/usr/bin/python3 $HERE/two_state_terminal_relay.py --runtime $RUNTIME --watch
Restart=always
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true
Environment=HIVE_PIPE_ALLOWED_ROOTS=$PROJECT
[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now one-wave-live-machine-executor.service
echo LIVE_MACHINE_EXECUTOR_INSTALLED
systemctl --user is-active one-wave-live-machine-executor.service

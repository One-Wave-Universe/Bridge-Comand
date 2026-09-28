#!/usr/bin/env bash
set -euo pipefail

SYSTEMD_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
SERVICE="$SYSTEMD_DIR/desktop-commander-remote.service"
SESSION="$HOME/.desktop-commander-device/device.json"

command -v node >/dev/null 2>&1 || { echo "DESKTOP_COMMANDER_HOLD: Node.js 18+ required" >&2; exit 2; }
command -v npx >/dev/null 2>&1 || { echo "DESKTOP_COMMANDER_HOLD: npx required" >&2; exit 2; }
major="$(node -p 'process.versions.node.split(".")[0]')"
(( major >= 18 )) || { echo "DESKTOP_COMMANDER_HOLD: Node.js 18+ required" >&2; exit 2; }
[[ -s "$SESSION" ]] || { echo "DESKTOP_COMMANDER_HOLD: saved Remote Device authorization missing at $SESSION" >&2; exit 3; }

mkdir -p "$SYSTEMD_DIR"
cat >"$SERVICE" <<EOF
[Unit]
Description=Desktop Commander Remote Device
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=0

[Service]
Type=simple
ExecStart=/usr/bin/env npx -y @wonderwhy-er/desktop-commander@latest remote
Restart=always
RestartSec=5
TimeoutStartSec=90
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now desktop-commander-remote.service
systemctl --user restart desktop-commander-remote.service
echo DESKTOP_COMMANDER_REMOTE_INSTALLED
systemctl --user is-active desktop-commander-remote.service

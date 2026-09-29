#!/usr/bin/env bash
set -euo pipefail

VERSION="${DESKTOP_COMMANDER_VERSION:-0.2.51}"
UNIT_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
UNIT="$UNIT_DIR/desktop-commander-remote.service"
AGENT_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/desktop-commander-agent"
SESSION="$HOME/.desktop-commander-device/device.json"

command -v node >/dev/null 2>&1 || { echo "DESKTOP_COMMANDER_HOLD: Node.js 18+ required" >&2; exit 2; }
command -v npm >/dev/null 2>&1 || { echo "DESKTOP_COMMANDER_HOLD: npm required" >&2; exit 2; }
major="$(node -p 'process.versions.node.split(".")[0]')"
(( major >= 18 )) || { echo "DESKTOP_COMMANDER_HOLD: Node.js 18+ required" >&2; exit 2; }
[[ -s "$SESSION" ]] || { echo "DESKTOP_COMMANDER_HOLD: saved authorization missing at $SESSION" >&2; exit 3; }

mkdir -p "$UNIT_DIR" "$AGENT_ROOT"
npm install --prefix "$AGENT_ROOT" --omit=dev --no-audit --no-fund "@wonderwhy-er/desktop-commander@$VERSION"

cat >"$UNIT" <<EOF
[Unit]
Description=Remote Desktop Commander persistent agent
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=0

[Service]
Type=simple
Environment=HOME=$HOME
Environment=PATH=$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin
Environment=DC_REMOTE_DEVICE=true
WorkingDirectory=$HOME
ExecStart=$AGENT_ROOT/node_modules/.bin/desktop-commander remote
Restart=always
RestartSec=5
KillMode=control-group
TimeoutStopSec=20
NoNewPrivileges=true
UMask=0077

[Install]
WantedBy=default.target
EOF

loginctl enable-linger "$(id -un)"
systemctl --user daemon-reload
systemctl --user enable --now desktop-commander-remote.service
systemctl --user restart desktop-commander-remote.service

systemctl --user is-enabled desktop-commander-remote.service
systemctl --user is-active desktop-commander-remote.service
loginctl show-user "$(id -un)" -p Linger
echo "DESKTOP_COMMANDER_REMOTE_INSTALLED version=$VERSION"
echo "Activation still requires an external online-device query and harmless identity receipt."

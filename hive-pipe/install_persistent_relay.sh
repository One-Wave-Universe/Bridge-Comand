#!/usr/bin/env bash
set -euo pipefail

# Install a persistent Cloudflare named-tunnel service for Hive Pipe.
# Requires cloudflared plus an already-provisioned tunnel token in the local
# environment or protected config. Secrets are never written to the repository.
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
SYSTEMD_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/hive-pipe"
ENV_FILE="$CONFIG_DIR/relay.env"
SERVICE="$SYSTEMD_DIR/hive-pipe-relay.service"

command -v cloudflared >/dev/null 2>&1 || {
  echo "HIVE_PIPE_RELAY_HOLD: cloudflared is not installed" >&2
  exit 2
}

mkdir -p "$SYSTEMD_DIR" "$CONFIG_DIR"
chmod 700 "$CONFIG_DIR"

# Accept the token only from protected local state. This intentionally refuses
# quick tunnels because their public URL changes and cannot anchor a plugin.
if [[ -n "${HIVE_PIPE_TUNNEL_TOKEN:-}" ]]; then
  umask 077
  printf 'HIVE_PIPE_TUNNEL_TOKEN=%q\n' "$HIVE_PIPE_TUNNEL_TOKEN" >"$ENV_FILE"
fi
if [[ ! -s "$ENV_FILE" ]]; then
  echo "HIVE_PIPE_RELAY_HOLD: provision HIVE_PIPE_TUNNEL_TOKEN once in protected local state" >&2
  exit 3
fi
chmod 600 "$ENV_FILE"

cat >"$SERVICE" <<EOF
[Unit]
Description=One-Wave Hive Pipe persistent public relay
After=network-online.target hive-pipe-gateway.service
Wants=network-online.target
Requires=hive-pipe-gateway.service

[Service]
Type=simple
EnvironmentFile=$ENV_FILE
ExecStart=/usr/bin/env cloudflared tunnel --no-autoupdate run --token ${HIVE_PIPE_TUNNEL_TOKEN}
Restart=always
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now hive-pipe-relay.service
systemctl --user restart hive-pipe-relay.service

echo HIVE_PIPE_RELAY_INSTALLED
systemctl --user is-active hive-pipe-relay.service

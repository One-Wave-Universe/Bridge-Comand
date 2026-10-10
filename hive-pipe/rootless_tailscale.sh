#!/usr/bin/env bash
# Rootless Jetson Tailscale experiment; no sudo, no system service changes.
set -euo pipefail
ARCHIVE="${1:?Usage: rootless_tailscale.sh /path/to/tailscale_arm64.tgz SHA256}"
EXPECTED="${2:?Provide expected SHA256 from trusted download source}"
BASE="${HOME}/.local/share/one-wave-tailscale"
mkdir -p "$BASE"
printf '%s  %s\n' "$EXPECTED" "$ARCHIVE" | sha256sum -c -
tar -tzf "$ARCHIVE" | grep -E '/(tailscale|tailscaled)$' >/dev/null
tar -xzf "$ARCHIVE" -C "$BASE"
DAEMON="$(find "$BASE" -type f -name tailscaled -print -quit)"
CLIENT="$(find "$BASE" -type f -name tailscale -print -quit)"
test -n "$DAEMON" && test -n "$CLIENT"
SOCKET="$BASE/tailscaled.sock"
STATE="$BASE/state"
if ! "$CLIENT" --socket="$SOCKET" status >/dev/null 2>&1; then
  nohup "$DAEMON" --tun=userspace-networking --socket="$SOCKET" --state="$STATE" >"$BASE/daemon.log" 2>&1 </dev/null &
  sleep 3
fi
echo "Authentication may require opening a URL on your phone."
"$CLIENT" --socket="$SOCKET" up
echo "Check connectivity:"
"$CLIENT" --socket="$SOCKET" status
echo "Do NOT expose Hive Pipe with Funnel until HTTPS, auth and external receipt checks pass."

#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$ROOT/hive-pipe/queue"/{pending,processing,results,done,failed}
mkdir -p "$HOME/.config/systemd/user"
sed "s|%h/Bridge-Comand|$ROOT|g" "$ROOT/hive-pipe/bridge-watchdog.service" > "$HOME/.config/systemd/user/one-wave-bridge-watchdog.service"
cp "$ROOT/hive-pipe/bridge-watchdog.timer" "$HOME/.config/systemd/user/one-wave-bridge-watchdog.timer"
systemctl --user daemon-reload
systemctl --user enable --now one-wave-bridge-watchdog.timer
python3 "$ROOT/hive-pipe/bridge_doctor.py" --repair --probe

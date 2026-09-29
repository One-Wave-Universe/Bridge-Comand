#!/usr/bin/env bash
set -u
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/one-wave-bootstrap"
mkdir -p "$STATE_DIR"
STAMP="$STATE_DIR/last-run.json"
PROJECT="${ONE_WAVE_PROJECT_ROOT:-/home/Scales/One-Wave-Science}"

active(){ systemctl --user is-active --quiet "$1"; }
restart(){ systemctl --user restart "$1" >/dev/null 2>&1 || true; }

# FIELD: healthy receiver exists. VOID: repair from locally installed authority.
phase=FIELD
if ! active one-wave-chatgpt-terminal-pull.service || ! active hive-pipe-gateway.service; then
 phase=VOID
 # Reinstall definitions from the local Bridge-Comand checkout. Network-dependent
 # relay installation remains nonfatal; the Git pull receiver is the durable path.
 ONE_WAVE_PROJECT_ROOT="$PROJECT" bash "$HERE/bootstrap_chatgpt_terminal_pull.sh" >/dev/null 2>&1 || true
 restart hive-pipe-agent.service
 restart hive-pipe-gateway.service
 restart one-wave-chatgpt-terminal-pull.service
 systemctl --user start one-wave-route-goblin.service >/dev/null 2>&1 || true
 systemctl --user start one-wave-bridge-lattice-watchdog.service >/dev/null 2>&1 || true
fi

pull=false; gateway=false; agent=false
active one-wave-chatgpt-terminal-pull.service && pull=true
active hive-pipe-gateway.service && gateway=true
active hive-pipe-agent.service && agent=true
if $pull && $gateway; then phase=FIELD; rc=0; else phase=VOID; rc=2; fi
printf '{"schema":"one-wave-bootstrap-receipt/v1","phase":"%s","pull":%s,"gateway":%s,"agent":%s,"time":"%s"}\n' "$phase" "$pull" "$gateway" "$agent" "$(date -u +%FT%TZ)" | tee "$STAMP"
exit "$rc"

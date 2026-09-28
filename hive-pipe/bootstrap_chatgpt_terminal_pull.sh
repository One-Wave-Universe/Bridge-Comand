#!/usr/bin/env bash
set -euo pipefail

# Safe bootstrap for a Jetson checkout whose current branch may be diverged.
# It fetches bridge code from origin/main without merging/resetting the active checkout.
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$PROJECT_ROOT" ]]; then
  echo "Run this from inside the One-Wave-Science checkout." >&2
  exit 2
fi

git -C "$PROJECT_ROOT" fetch origin main
ONE_WAVE_PROJECT_ROOT="$PROJECT_ROOT" \
  BRIDGE_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
ONE_WAVE_PROJECT_ROOT="$PROJECT_ROOT" bash "$BRIDGE_ROOT/hive-pipe/install_chatgpt_terminal_pull.sh"
bash "$BRIDGE_ROOT/hive-pipe/install_bridge_lattice_watchdog.sh"

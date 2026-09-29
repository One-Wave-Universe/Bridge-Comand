#!/usr/bin/env bash
set -euo pipefail

# Bootstrap from Bridge-Comand while leaving the active Science checkout alone.
BRIDGE_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
if [[ -d "$BRIDGE_ROOT/.git" ]]; then
  git -C "$BRIDGE_ROOT" fetch origin main
  git -C "$BRIDGE_ROOT" checkout --detach origin/main
fi
PROJECT_ROOT="${ONE_WAVE_PROJECT_ROOT:-}"
if [[ -z "$PROJECT_ROOT" ]]; then
  # Prefer the canonical Science checkout; fall back to current repo only when
  # explicitly running there.
  for candidate in "$HOME/One-Wave-Science" "$HOME/One_Wave_Science"; do
    [[ -d "$candidate/.git" ]] && PROJECT_ROOT="$candidate" && break
  done
fi
if [[ -z "$PROJECT_ROOT" || ! -d "$PROJECT_ROOT/.git" ]]; then
  echo "BOOTSTRAP_HOLD: set ONE_WAVE_PROJECT_ROOT to the One-Wave-Science checkout" >&2
  exit 2
fi

ONE_WAVE_PROJECT_ROOT="$PROJECT_ROOT" bash "$BRIDGE_ROOT/hive-pipe/install_gateway.sh"
ONE_WAVE_PROJECT_ROOT="$PROJECT_ROOT" bash "$BRIDGE_ROOT/hive-pipe/install_chatgpt_terminal_pull.sh"
bash "$BRIDGE_ROOT/hive-pipe/install_persistent_relay.sh" || true
bash "$BRIDGE_ROOT/hive-pipe/install_bridge_lattice_watchdog.sh"
bash "$BRIDGE_ROOT/hive-pipe/install_route_goblin.sh"
ONE_WAVE_PROJECT_ROOT="$PROJECT_ROOT" bash "$BRIDGE_ROOT/hive-pipe/install_independent_bootstrap.sh"
ONE_WAVE_PROJECT_ROOT="$PROJECT_ROOT" bash "$BRIDGE_ROOT/hive-pipe/install_live_machine_executor.sh" || true

python3 "$BRIDGE_ROOT/hive-pipe/bridge_lattice_watchdog.py" || true
echo BRIDGE_LATTICE_BOOTSTRAP_COMPLETE

#!/usr/bin/env bash
set -euo pipefail

BRIDGE_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
PROJECT_ROOT="${ONE_WAVE_PROJECT_ROOT:-}"

if [[ ! -d "$BRIDGE_ROOT/.git" ]]; then
  echo "BOOTSTRAP_HOLD: canonical Bridge-Comand checkout is missing" >&2
  exit 2
fi
case "$(git -C "$BRIDGE_ROOT" remote get-url origin 2>/dev/null || true)" in
  *One-Wave-Universe/Bridge-Comand*) ;;
  *) echo "BOOTSTRAP_HOLD: unexpected Bridge-Comand origin" >&2; exit 2 ;;
esac

if [[ -z "$PROJECT_ROOT" ]]; then
  for candidate in \
    "$HOME/One-Wave-Science" \
    "$HOME/Downloads/One-Wave-Science" \
    "/home/Scales/One-Wave-Science"
  do
    if [[ -d "$candidate/.git" ]]; then
      PROJECT_ROOT="$candidate"
      break
    fi
  done
fi
if [[ -z "$PROJECT_ROOT" || ! -d "$PROJECT_ROOT/.git" ]]; then
  echo "BOOTSTRAP_HOLD: set ONE_WAVE_PROJECT_ROOT to the One-Wave-Science checkout" >&2
  exit 2
fi

# Install services from this exact canonical checkout. Do not clone, detach,
# reset, or replace either owning repository during recovery.
ONE_WAVE_PROJECT_ROOT="$PROJECT_ROOT" bash "$BRIDGE_ROOT/hive-pipe/install_gateway.sh"
ONE_WAVE_PROJECT_ROOT="$PROJECT_ROOT" bash "$BRIDGE_ROOT/hive-pipe/install_chatgpt_terminal_pull.sh"
bash "$BRIDGE_ROOT/hive-pipe/install_persistent_relay.sh" || true
bash "$BRIDGE_ROOT/hive-pipe/install_bridge_lattice_watchdog.sh"
bash "$BRIDGE_ROOT/hive-pipe/install_route_goblin.sh"
ONE_WAVE_PROJECT_ROOT="$PROJECT_ROOT" bash "$BRIDGE_ROOT/hive-pipe/install_independent_bootstrap.sh"
ONE_WAVE_PROJECT_ROOT="$PROJECT_ROOT" bash "$BRIDGE_ROOT/hive-pipe/install_live_machine_executor.sh" || true

python3 "$BRIDGE_ROOT/hive-pipe/bridge_lattice_watchdog.py" || true
echo BRIDGE_LATTICE_BOOTSTRAP_COMPLETE

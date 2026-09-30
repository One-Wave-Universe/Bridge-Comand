#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "ERROR: run inside Bridge-Comand" >&2
  exit 2
}
cd "$ROOT"
REMOTE="$(git remote get-url origin 2>/dev/null || true)"
case "$REMOTE" in
  *One-Wave-Universe/Bridge-Comand*) ;;
  *) echo "ERROR: Brain Buddy runtime must be Bridge-Comand: $REMOTE" >&2; exit 2 ;;
esac
exec python3 brain_buddy/brain_buddy_council.py "$@"

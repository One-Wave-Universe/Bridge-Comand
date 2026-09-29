#!/usr/bin/env bash
set -euo pipefail

HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
BRIDGE_ROOT="$(CDPATH= cd -- "$HERE/.." && pwd)"

if [[ ! -d "$BRIDGE_ROOT/.git" ]]; then
  echo "Run this installer from the canonical Bridge-Comand checkout." >&2
  exit 2
fi
case "$(git -C "$BRIDGE_ROOT" remote get-url origin 2>/dev/null || true)" in
  *One-Wave-Universe/Bridge-Comand*) ;;
  *) echo "Unexpected Bridge-Comand origin." >&2; exit 2 ;;
esac

SCIENCE_ROOT="${ONE_WAVE_PROJECT_ROOT:-}"
if [[ -z "$SCIENCE_ROOT" ]]; then
  for candidate in \
    "$HOME/One-Wave-Science" \
    "$HOME/Downloads/One-Wave-Science" \
    "/home/Scales/One-Wave-Science"
  do
    if [[ -d "$candidate/.git" ]] && git -C "$candidate" remote get-url origin 2>/dev/null | grep -q 'One-Wave-Science'; then
      SCIENCE_ROOT="$candidate"
      break
    fi
  done
fi
if [[ -z "$SCIENCE_ROOT" || ! -d "$SCIENCE_ROOT/.git" ]]; then
  echo "One-Wave-Science checkout not found; set ONE_WAVE_PROJECT_ROOT." >&2
  exit 2
fi
SCIENCE_ROOT="$(CDPATH= cd -- "$SCIENCE_ROOT" && pwd)"
TRANSPORT_URL="$(git -C "$SCIENCE_ROOT" remote get-url origin)"

if git -C "$BRIDGE_ROOT" remote get-url transport >/dev/null 2>&1; then
  git -C "$BRIDGE_ROOT" remote set-url transport "$TRANSPORT_URL"
else
  git -C "$BRIDGE_ROOT" remote add transport "$TRANSPORT_URL"
fi
git -C "$BRIDGE_ROOT" fetch --prune transport chatgpt-terminal chatgpt-terminal-backup

STATE_ROOT="${XDG_STATE_HOME:-$HOME/.local/state}/one-wave-chatgpt-terminal"
EXTERNAL_ROOT="${ONE_WAVE_EXTERNAL_WORK:-$HOME/One-Wave-External-Work}"
UNIT_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
UNIT="$UNIT_DIR/one-wave-chatgpt-terminal-pull.service"
mkdir -p "$STATE_ROOT" "$UNIT_DIR" "$EXTERNAL_ROOT/inbox" "$EXTERNAL_ROOT/work" "$EXTERNAL_ROOT/outbox"

cat >"$UNIT" <<EOF
[Unit]
Description=One-Wave resilient ChatGPT terminal bridge
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=0

[Service]
Type=simple
WorkingDirectory=$BRIDGE_ROOT
ExecStart=/usr/bin/python3 $HERE/chatgpt_terminal_pull.py --watch
Restart=always
RestartSec=5
TimeoutStartSec=45
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$BRIDGE_ROOT $STATE_ROOT $SCIENCE_ROOT $EXTERNAL_ROOT
Environment=PYTHONUNBUFFERED=1
Environment=CHATGPT_TERMINAL_DEFAULT_CWD=$SCIENCE_ROOT
Environment=CHATGPT_TERMINAL_ROUTES=primary=transport:chatgpt-terminal,backup=transport:chatgpt-terminal-backup
Environment=HIVE_PIPE_ALLOWED_ROOTS=$SCIENCE_ROOT:$EXTERNAL_ROOT
Environment=ONE_WAVE_PROJECT_ROOT=$SCIENCE_ROOT
Environment=REFERENCE_GATE_LEDGER=$STATE_ROOT/reference-receipts.jsonl

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now one-wave-chatgpt-terminal-pull.service
systemctl --user restart one-wave-chatgpt-terminal-pull.service

printf 'CHATGPT_TERMINAL_PULL_INSTALLED\n'
printf 'bridge=%s\n' "$BRIDGE_ROOT"
printf 'science=%s\n' "$SCIENCE_ROOT"
printf 'routes=transport:chatgpt-terminal,transport:chatgpt-terminal-backup\n'
systemctl --user is-active one-wave-chatgpt-terminal-pull.service

for attempt in 1 2 3 4 5; do
  if python3 "$HERE/bridge_doctor.py" --profile pull; then
    printf 'CHATGPT_TERMINAL_PULL_HEALTHY\n'
    exit 0
  fi
  sleep 2
done

echo "Bridge service started but did not pass its live pull profile." >&2
echo "Inspect: journalctl --user -u one-wave-chatgpt-terminal-pull.service -n 100 --no-pager" >&2
exit 1

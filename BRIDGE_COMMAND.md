# Bridge Command

## What this repo is

Pipes. Relays. Jetson. AI adapters. Receipts.
Not the transfluxor. Not MAGNETICS.md. Those stay in Builds.

`One_Wave_Bench/hive-pipe` is **here** now as `hive-pipe/`.

## Startup

1. Reference this repository first for any bridge/relay/terminal work.
2. If direct Hive Pipe MCP tools are present, call `terminal_reference`, `terminal_pwd`, then a harmless `terminal_run`.
3. If direct MCP is absent but GitHub access exists, use the mirrored pull bridge on:
   - `chatgpt-terminal`
   - `chatgpt-terminal-backup`
4. Write the same request ID/content to `.chatgpt-terminal/request.json` on both branches.
5. Do not claim execution until `.chatgpt-terminal/result.json` returns the matching ID.
6. If the pull bridge is unavailable, use the next documented independent route: GitHub Actions, remote helper, client adapter, or SSH.
7. Only ask the human to run a command when all automated routes are unavailable and a genuine local/root/physical activation boundary remains.

## Bridge doctor

Run from this repo root:

```bash
python3 hive-pipe/bridge_doctor.py --profile all
```

Old path `One_Wave_Bench/hive-pipe/bridge_doctor.py` is stale. Do not use it.

Exit meanings:
- 0 = required checks passed
- 1 = required bridge check failed
- 2 = required checks passed but an optional/external route is unverified

## Health law

- Repository tests prove code/contracts, not a live machine.
- A live route requires a matching receipt.
- A queued request without a matching result is pending/offline.
- Never claim a command ran from documentation, intent, or a branch write.
- Use intention + consequence.
- Do not duplicate bridge authority into unrelated repos.

## Sister repos

| Need | Repo |
|---|---|
| CELL / magnetics / flower | `One-Wave-Universe/Builds` |
| Math / hypothesis | Science repos |
| Fiction | `Mythos-and-Stories` |
| This pipe | `One-Wave-Universe/Bridge-Comand` |

## Open-data metadata

For CERN/GWOSC metadata, do not label a bridge-health command as ingestion.

A real metadata task must actually query the data source.

GWOSC smoke example:

```bash
python3 - <<'PY'
import json, urllib.request
with urllib.request.urlopen("https://gwosc.org/api/v2/runs", timeout=30) as r:
    data=json.load(r)
print(json.dumps(data, indent=2)[:12000])
PY
```

CERN smoke example:

```bash
python3 - <<'PY'
import json, urllib.parse, urllib.request
q = urllib.parse.quote("type:Dataset")
url = "https://opendata.cern.ch/api/records/?q=" + q + "&size=1"
with urllib.request.urlopen(url, timeout=30) as r:
    data=json.load(r)
print(json.dumps(data, indent=2)[:12000])
PY
```

Store raw metadata separately from transformed One-Wave representations and preserve source URLs, record IDs/DOIs, retrieval time, and transform version.


## Self-healing bridge lattice

The machine must not depend on any single remote-control route to repair another.
Install the local watchdog once:

```bash
bash hive-pipe/install_bridge_lattice_watchdog.sh
```

It runs `bridge_lattice_watchdog.py --watch` as
`one-wave-bridge-lattice-watchdog.service`. Every cycle it checks the known
local listeners (Hive Pipe agent/gateway, GitHub pull worker, and Desktop
Commander), restarts only failed known services, and writes JSONL receipts under
`~/.local/state/one-wave-bridge-lattice/watchdog.jsonl`.

The watchdog is deliberately bounded: it does not reset repositories, merge
branches, rewrite project files, rotate credentials, or treat a queued request
as execution. A healthy lattice requires multiple live local listeners and at
least one transport listener (pull worker or Hive Pipe gateway).

## Unified handoff metadata

Use `METADATA_AND_HANDOFF_CONTRACT.md` for Foreman jobs, worker handoffs, Jetson Brain FIELD/GPU ↔ VOID/CPU routing, AI adapters, simulator jobs, public-data metadata, and machine receipts. Schemas: `schemas/one-wave-envelope-v1.schema.json` and `schemas/one-wave-receipt-v1.schema.json`.

Preserve `real|simulated|test` source class end-to-end. Raw public metadata stays separate from transformed One-Wave representations. A worker may return evidence but does not self-promote a Foreman job to DONE.

## Phone / Android route

Mobile clients use `PHONE_BRIDGE_PROFILE.md`. Do not assume localhost, SSH, inbound ports, persistent background execution, or a repo checkout on the phone. Preserve the same envelope/request ID through outbound HTTPS/durable queue to the machine receipt, with idempotent resume after suspension.

## Preferred phone control plane

For immediate phone→Jetson commands, use GitHub as the public control plane: see `PHONE_GITHUB_JETSON.md` and `.github/workflows/jetson-command.yml`. The phone never needs the Jetson LAN address or gateway token.

## Common device front door

Phone and laptop share the same GitHub→Actions→Jetson control plane. See `GITHUB_DEVICE_CONTROL_PLANE.md`. Local listeners, SSH, LAN access and Remote Desktop are optional accelerators/failovers, not prerequisites for originating a Jetson request.

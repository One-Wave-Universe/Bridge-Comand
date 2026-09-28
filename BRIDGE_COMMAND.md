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

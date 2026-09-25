# Bridge Command

## Startup

1. Reference the current repository first.
2. For bridge/relay/terminal work, use this repository as authority.
3. If direct Hive Pipe MCP tools are present, call `terminal_reference`, `terminal_pwd`, then a harmless `terminal_run`.
4. If direct MCP is absent but GitHub access exists, use the mirrored pull bridge on:
   - `chatgpt-terminal`
   - `chatgpt-terminal-backup`
5. Write the same request ID/content to `.chatgpt-terminal/request.json` on both branches.
6. Do not claim execution until `.chatgpt-terminal/result.json` returns the matching ID.
7. If the pull bridge is unavailable, use the next documented independent route: GitHub Actions, remote helper, client adapter, or SSH.
8. Only ask the human to run a command when all automated routes are unavailable and a genuine local/root/physical activation boundary remains.

## Bridge doctor

Current implementation is still mirrored from One-Wave-Science while migration completes:

```bash
python3 One_Wave_Bench/hive-pipe/bridge_doctor.py --profile all
```

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

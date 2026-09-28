# One-Wave AI Bridge / Relay Start Here

## Authority

Bridge and relay authority is:

`One-Wave-Universe/Bridge-Comand`

Current live Hive Pipe runtime may be installed into a generated runtime/worktree, so do not assume the running process path from documentation. Use the doctor and the returned receipt.

## First action

From a Bridge-Comand checkout:

```bash
python3 hive-pipe/bridge_doctor.py --profile all
```

Machine readable:

```bash
python3 hive-pipe/bridge_doctor.py --profile all --json
```

Exit meanings:

- `0`: required checks passed.
- `1`: required bridge check failed.
- `2`: required checks passed but a non-critical route could not be verified.

## No-direct-terminal rule

"No direct terminal tool in this chat" is **not** a stop condition.

Use the next route the AI actually has:

1. Direct Hive Pipe MCP: `terminal_reference`, `terminal_pwd`, `terminal_run`.
2. GitHub pull bridge: `chatgpt-terminal` + `chatgpt-terminal-backup`.
3. Remote Desktop Commander / authorized remote-computer route.
4. GitHub Actions Jetson Command Lane.
5. Client adapter: Gemini, DeepSeek, Codex, Claude, Perplexity.
6. SSH recovery.

Only ask the human to run an ordinary command after the available automated routes have actually been checked.

## Direct Hive Pipe

Local endpoint:

`http://127.0.0.1:8765/mcp`

Core tools:

`terminal_reference`, `terminal_pwd`, `terminal_which`, `terminal_run`, `python_run`, `cpp_compile_run`.

For executable commands, include `intention` and `consequence` when the active parser contract requires them.

A route is live only after a real receipt returns stdout/stderr/exit status.

## Pull bridge

Transport branches remain on `One-Wave-Universe/One-Wave-Science` while migration is completed:

- `chatgpt-terminal`
- `chatgpt-terminal-backup`

Write the same request to `.chatgpt-terminal/request.json` on both branches. Use the same request ID and content.

Read `.chatgpt-terminal/result.json` on both branches. Do not claim execution unless one returns the matching request ID.

## Remote-computer bridge

If Remote Desktop Commander is available, use it instead of asking the human to relay commands. Verify the target device, then inspect the checkout and execute bounded commands there.

## GitHub Actions

Workflow:

`.github/workflows/jetson-command.yml`

A workflow definition is not proof of a live route. Require expected stdout and exit code 0 from the dispatched run.

## DeepSeek

Official API adapter:

```bash
python3 hive-pipe/deepseek_bridge.py --mcp-smoke
```

Web relay adapter:

```bash
python3 hive-pipe/deepseek_web_bridge.py --relay-health --mcp-smoke
```

## Metadata routes

CERN Open Data and GWOSC/LIGO metadata are public-data tasks, not bridge-health tasks.

A bridge-doctor command must not be labeled as "metadata ingest."

The proven bounded metadata cache location on the Jetson is:

`/home/Scales/One-Wave-Science/.one-wave-metadata/`

A valid ingest must actually query the public endpoint, persist raw metadata separately, and record source URLs and retrieval time.

## Health law

- Repository code/tests are not proof of a live machine.
- A queued request without a matching result is pending/offline.
- A live route requires a matching receipt from that route.
- Do not invent success from documentation or intent.
- Do not expose tokens or credentials.
- Do not duplicate bridge authority into Science after migration.

## Unified handoff metadata

Use `METADATA_AND_HANDOFF_CONTRACT.md` for Foreman jobs, worker handoffs, Jetson Brain FIELD/GPU ↔ VOID/CPU routing, AI adapters, simulator jobs, public-data metadata, and machine receipts. Schemas: `schemas/one-wave-envelope-v1.schema.json` and `schemas/one-wave-receipt-v1.schema.json`.

Preserve `real|simulated|test` source class end-to-end. Raw public metadata stays separate from transformed One-Wave representations. A worker may return evidence but does not self-promote a Foreman job to DONE.

## Phone / Android route

Mobile clients use `PHONE_BRIDGE_PROFILE.md`. Do not assume localhost, SSH, inbound ports, persistent background execution, or a repo checkout on the phone. Preserve the same envelope/request ID through outbound HTTPS/durable queue to the machine receipt, with idempotent resume after suspension.

## Common device front door

Phone and laptop share the same GitHub→Actions→Jetson control plane. See `GITHUB_DEVICE_CONTROL_PLANE.md`. Local listeners, SSH, LAN access and Remote Desktop are optional accelerators/failovers, not prerequisites for originating a Jetson request.

## Device lattice

Load `DEVICE_LATTICE.md` for cross-device routing. Phone, laptop and Jetson are addressable lattice nodes through GitHub; preserve one request ID, provenance and chained hop receipts across every route. “Open” means authenticated/routable, never unauthenticated shell exposure.

## AI route discovery

AI agents: load `AI_ROUTING.md` first for device work and parse `ai-route-manifest.json` when a machine-readable route map is useful. Do not stop merely because one listener/route is unavailable; use the authorized lattice failover rules and require a matching final-target receipt.

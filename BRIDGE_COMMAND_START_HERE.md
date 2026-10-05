# Bridge Command — Canonical Recovery and Operations

This repository is the single authority for One-Wave bridge, relay, remote-execution, metadata, and AI-to-AI transport work.

## Shared laptop fallback for clients without direct tools

See [Shared laptop access](hive-pipe/SHARED_LAPTOP_ACCESS.md). GitHub-only clients can push `.laptop-dispatch/request.json` on an isolated branch and read their own Laptop Command Relay job receipt. The Jetson relays the signed request to the Latitude; this targets the laptop rather than the old Jetson-only pull worker.

## Latest verified access — 2026-10-05

This section supersedes the dated September handover and missing-secret reports below.

- Desktop Commander: both `localhost.localdomain` (ARM/Jetson) and `scales-Latitude-E7450` returned terminal identity receipts on 2026-10-05. Use `list_devices`, then `start_process` with the selected device ID.
- Jetson local Hive Pipe: `bridge_doctor.py --profile all` returned `BRIDGE_DOCTOR_EXIT=0`, including the exact gateway marker and reachable primary/backup Git transport branches. Branch reachability alone does not establish a fresh pull-mailbox round trip.
- Moved GitHub workflows: `JETSON_GATEWAY_URL` and `JETSON_GATEWAY_TOKEN` were missing in Bridge-Comand while present in Science. Both are now configured in Bridge-Comand from the live tunnel and existing protected Codex token; no token was regenerated or committed.
- GitHub -> public relay -> Jetson terminal -> GitHub receipt: [run 37387521891](https://github.com/One-Wave-Universe/Bridge-Comand/actions/runs/37387521891) succeeded with `BRIDGE_GITHUB_20261005_OK`, exit 0, cwd `/home/Scales/One-Wave-Science`.
- Jetson metadata listing through the moved workflow: [run 37387525171](https://github.com/One-Wave-Universe/Bridge-Comand/actions/runs/37387525171) succeeded, returned metadata paths, and exited 0. This proves metadata-file access, not every external provider.
- Gateway, queue worker, quick tunnel, pull worker, live-machine executor, Desktop Commander, and DeepSeek peer services were active/enabled. Provider services being active does not prove a new model response. `GEMINI_API_KEY` and `OPENAI_API_KEY` secret names exist in Bridge-Comand; their provider validity was not tested here.
- Bootstrap, route-goblin, and bridge-watchdog timers were scheduled and running. Their oneshot services can legitimately be inactive between timer ticks.

### Commands for the next AI

Workflows belong to `One-Wave-Universe/Bridge-Comand`; science commands use cwd `/home/Scales/One-Wave-Science`, and build commands use the owning Builds checkout. Dispatch `.github/workflows/jetson-command.yml` on `main` with `argv_json`, `cwd`, `timeout`, `intention`, and `consequence`. Read the completed job log and exact returned output before declaring success. Use `.github/workflows/jetson-science-metadata.yml` for metadata operations.

Remote Desktop Commander shells may lack user-service environment variables. On the verified ARM account, prefix user-systemd commands with `XDG_RUNTIME_DIR=/run/user/2002 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/2002/bus`. Obtain `id -u` and the runtime path afresh on other devices. Do not query system service state to classify user services.

The current relay is a quick tunnel. Its URL can change after restart. Obtain the current URL from system journal records for `_SYSTEMD_USER_UNIT=hive-pipe-cloudflared.service`; the old `~/.local/state/hive-pipe/cloudflared.log` was stale. Probe it with the saved token before updating repository secrets. Synchronize credentials to the repository that owns the workflow. A stable named tunnel and automatic URL-secret synchronization remain unverified.

## Operating law

REFERENCE GIT -> ASK/PIVOT -> REFERENCE METADATA/CENTER-FLIP -> VALIDATE/PIVOT -> UPDATE REFERENCE/CENTER-FLIP -> REFERENCE.

Every flip returns through the reference. Do not declare a bridge healthy because files, services, queues, or workflows exist. A route is healthy only after an end-to-end receipt from the requested endpoint.

## One authority, live connections, no copies

- Bridge-Comand owns bridge and relay contracts.
- One-Wave-Science owns science claims, models, evidence rules, and scientific source interpretation.
- Builds owns runnable build artifacts.
- A device service must point to the canonical existing checkout or an explicitly named runtime cache. A runtime cache is never a second authority.
- Do not create another bridge repository, paste bridge doctrine into Science, or treat a generated worktree as canon.
- Connect agents to the owning repository and record the repository URL, branch, commit SHA, and reference files in every receipt.

## Directions for every AI client

Codex, ChatGPT, Gemini, Claude, DeepSeek, Perplexity, local Qwen/OpenClaw, phone relays, and future clients use the same loop:

1. Read this file and the owning repository's canonical start file.
2. Record repository, branch, commit SHA, exact question, and named reference paths.
3. Ask the bounded question through the smallest live lane.
4. When a conclusion depends on measured numbers, declare `numeric_evidence_required: true` and attach bounded science metadata requests. Do not invent, remember, or silently substitute numbers.
5. Keep provider material separate from One-Wave interpretations.
6. Validate the response against the named repository references and metadata provenance.
7. Return a receipt containing route, request ID, references actually read, metadata actually read, exit/result state, and unresolved gaps.
8. Update only the owning repository when warranted, then reference the new commit again.

Required status words are: `ESTABLISHED`, `IMPLEMENTED`, `TESTED`, `UNVERIFIED`, `HYPOTHESIS`, `ASSUMPTION`, `FAILED`, and `BLOCKED`.

## Terminal availability is per session

Discover the calling AI's own tools first. Another AI's Desktop Commander device
receipt does not attach tools to this session. Use a direct device terminal when
exposed; a GitHub-only client uses the configured pull relay and requires its own
matching return. Science's [terminal entrypoint](https://github.com/One-Wave-Universe/One-Wave-Science/blob/main/AI_BRIDGE_START_HERE.md)
provides the device selection examples.

Pull intake and result delivery have independent circuit-breaker state:
`read_routes` governs fetch/poll; `routes` governs publication. Missing write
credentials may block delivery without preventing a read-only route from
accepting and executing a bounded request. Completed results remain in the
durable outbox. A matching connector-published result can reconcile completion
without re-execution. Delayed old results are archived and cannot replace a
newer request's current result.

The connector-assisted return is an explicit recovery lane: an authorized client
reads a real target receipt and publishes that exact ID/digest through its GitHub
connector. It is not proof that the target's unattended git push works.
See [the recovery receipt](hive-pipe/PULL_RECOVERY_2026-10-04.md) for execution,
deployment and the remaining authentication boundary.

## Current lanes

### Jetson / Hive Pipe MCP

Canonical remote contract uses Hive Pipe MCP `terminal_run`.
Required command fields: `argv`, `timeout`, `intention`, `consequence`; `cwd` when needed.
Never put credentials in tracked files or logs.

Expected Jetson credential locations:

- `~/.config/hive-pipe/tokens/codex.token`
- legacy migration source: `~/.config/hive-pipe/gateway.token`
- optional client environment: `~/.config/hive-pipe/remote.env`

GitHub Actions expects repository secrets `JETSON_GATEWAY_URL` and `JETSON_GATEWAY_TOKEN`. Restore them from the live Jetson configuration. Never manufacture a replacement token merely to make a test pass. Never commit their values.

### Desktop Commander

Registered machines may exist while their transports are offline. Treat registration/auth-token validity, process state, service state, and transport-online state separately.

Persistent unit on both Linux devices:

`~/.config/systemd/user/desktop-commander-remote.service`

Required service properties:

- pinned agent version;
- `Restart=always`;
- enabled for `default.target`;
- user linger enabled so the service survives logout and starts at boot;
- saved registration under the user's home directory;
- no copied One-Wave repository.

Recovery order:

1. Query device state.
2. If online, run `hostname` and `id -un` and retain the receipt.
3. Inspect `systemctl --user show desktop-commander-remote.service -p ActiveState -p SubState -p UnitFileState -p MainPID -p ExecMainStatus`.
4. If offline, use an independent live lane to restart that service once.
5. Query device state again.
6. Run the harmless identity probe again.
7. Only then mark Desktop Commander `VERIFIED`.

Current handover state on 2026-09-29:

- `scales-Latitude-E7450` and `localhost.localdomain` have valid saved registrations.
- pinned version `0.2.51` user services were installed, enabled, active, and both accounts had `Linger=yes` before handover.
- after the old manual processes were terminated, both registered devices reported offline and did not reconnect within the observation window.
- therefore persistent Desktop Commander transport is `PARTIAL`, not verified. The first failing boundary is service-process-to-remote-transport reconnection. Restart the service from an independent lane and require a new online identity receipt.

### GitHub pull bridge

Primary and backup transport branches remain `chatgpt-terminal` and `chatgpt-terminal-backup` in One-Wave-Science until migration is explicitly completed. Write the same request ID and content to both and require a matching result ID. A stale result is not a response.

### GitHub Actions -> Jetson metadata

Active workflow: `.github/workflows/jetson-science-metadata.yml`.
Request directory: `.metadata-dispatch/`.

A live query must use a bounded HTTPS metadata/API endpoint. The Jetson performs the external query; GitHub is the dispatch/reference layer.

Current verified state:

- GitHub push dispatch works.
- run `36567405790` failed before Jetson contact because `JETSON_GATEWAY_URL` and `JETSON_GATEWAY_TOKEN` were absent.
- GitHub -> Jetson metadata transport remains `BLOCKED`, not end-to-end verified.

### Gemini repository lens

Gemini must use One-Wave-Science as a lens, not replace it:

`REFERENCE GIT -> ASK -> GEMINI RESPONSE -> VALIDATE AGAINST REFERENCE/METADATA -> UPDATE OWNING REPO IF WARRANTED -> REFERENCE`.

The GitHub-native request schema accepts named repository references and optional bounded science metadata:

```json
{
  "schema": "one-wave-github-gemini/v2",
  "id": "unique-request-id",
  "question": "One bounded question",
  "references": [
    {
      "repo": "One-Wave-Universe/One-Wave-Science",
      "ref": "main",
      "path": "exact/relevant/file.md"
    }
  ],
  "numeric_evidence_required": true,
  "metadata_requests": [
    {
      "provider": "GWOSC",
      "url": "https://gwosc.org/api/v2/event-versions/",
      "purpose": "Identify the exact catalog/event metadata needed by the question",
      "max_bytes": 250000
    }
  ]
}
```

The workflow automatically reads `One-Wave-Science/AI_CANONICAL_START_HERE.md` first, records every reference and metadata source actually read, hashes retrieved metadata, and tells Gemini to label evidence state. Metadata is consulted only when the request declares that measured numbers are required.

Current verified state:

- run `36566722396` reached the Gemini job but failed because `GEMINI_API_KEY` was absent.
- a queued request or workflow start is not a Gemini response.
- the Jetson CLI/OAuth lane is separate and must return its own matching receipt.

## Science metadata rules

Before external data:

1. reference One-Wave-Science canon and the exact test;
2. query metadata before bulk data;
3. inspect size before data;
4. use the smallest useful sample;
5. preserve provider, experiment/detector, record/event/catalog/version IDs, URL/API endpoint, release/version, retrieval time, units/calibration/quality fields, byte count, and content hash;
6. keep raw provider material separate from One-Wave-derived transformations;
7. treat retrieval as input evidence, not automatic scientific support;
8. never tune a frozen prediction after exposure to held-out evidence.

## Failure discipline

Change one thing -> test -> compare to goal -> check drift.
After three repeats of the same failure, change route or diagnostic angle.
Prefer receipts over explanations.
Do not create duplicate bridge doctrine in other repositories; point back here.

## Definition of done

A bridge is `VERIFIED` only when the requested endpoint completes and its return is read back through the intended path. File presence, service configuration, registration validity, queue creation, and workflow launch are intermediate states only.

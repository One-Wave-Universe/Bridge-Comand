# Bridge Command — Canonical Recovery and Operations

This repository is the single authority for One-Wave bridge, relay, remote-execution, metadata, and AI-to-AI transport work.

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

## Reference -> Build -> Check — mandatory build law

For any build, repair, recovery, bridge, worker, Brain Buddy, or runtime task, **REFERENCE does not mean merely reading design documentation**. REFERENCE means reconstructing the authoritative real state that the next change must inherit.

Before writing or changing code, recover and record, in this order:

1. **Canonical authority** — this file plus the owning repository's canonical start/reference rules.
2. **Last successful observable result** relevant to the requested capability. Search receipts, responses, sessions, outputs, completed runs, workflow/job logs, and returned endpoint results. Prefer the last proven success over the latest commit.
3. **Receipt/result provenance** — request ID, timestamp, provider/worker, actual returned content/result, and acceptance condition that made it a success.
4. **Exact implementation that produced that result** — executable/entry point, caller, adapter/bridge/relay, trigger/listener/workflow/service, and state/session files.
5. **Exact source state** — repository, branch, commit SHA, and relevant file SHAs/paths.
6. **Exact execution path** — where execution starts, every transport boundary it crosses, where credentials/auth are supplied, and where the return comes back.
7. **Current divergence** — compare the known-good state to the current state and identify the first changed or broken boundary.

For recovery work, use this chain explicitly:

`LAST SUCCESSFUL RESPONSE -> RECEIPT/SESSION -> CODE THAT PRODUCED IT -> COMMIT SHA -> EXECUTION/TRIGGER PATH -> AUTH/TRANSPORT -> RE-RUN SAME PACKET -> MATCHING RETURN RECEIPT`

**Do not use "latest commit" as a substitute for known-good. Do not design a replacement from documentation while a prior working implementation can be recovered. Do not BUILD until the reference chain reaches a real executable entry point and its return path.**

### BUILD

Build from the recovered known-good source state on a new recovery/goal branch.

- Preserve the working entry point and return path unless the bounded task specifically requires changing them.
- Change the smallest boundary needed.
- Do not collapse providers, transports, authentication methods, worker identities, state, provenance, receipts, or evidence sources into a common mechanism merely because they serve a common Brain Buddy contract.
- Provider adapters remain provider-specific. A shared envelope is not permission to replace native transports.
- Never replace a working logged-in/session route with an API route, or an API route with a session route, without explicit evidence and an explicit task requiring that change.
- A build is incomplete if no reachable trigger/entry point can execute it.

### CHECK

CHECK means execute the real entry point through the intended path and observe the requested endpoint return.

- Source inspection, file existence, syntax success, queue creation, workflow launch, service-active state, listener presence, or dispatch success are **not** endpoint PASS.
- Require the same request ID across request and return when the contract supports it.
- Record actual transport, provider/worker identity, reference state, result, and failure boundary.
- If the endpoint does not return, mark `FAILED` or `BLOCKED`; do not describe the build as working.
- After CHECK, return to REFERENCE. The observed result becomes part of the next authoritative state.
- If CHECK fails, reference the last known-good chain again before the next BUILD. Do not stack speculative fixes.

The mandatory loop is:

`REFERENCE REAL STATE -> BUILD ONE BOUNDED CHANGE -> CHECK REAL ENDPOINT -> REFERENCE OBSERVED STATE -> ...`

For Brain Buddy specifically, the persistent back-and-forth architecture coordinates independent workers; the reference is the authoritative state each loop crosses, not a replacement for the architecture. Council is a set of participating workers/views, not the Brain Buddy architecture itself.

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

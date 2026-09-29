# Bridge Command — Canonical Recovery and Operations

This repository is the authority for One-Wave bridge, relay, remote-execution, metadata, and AI-to-AI transport work.

## Operating law

REFERENCE -> ASK/PIVOT -> REFERENCE METADATA/CENTER-FLIP -> VALIDATE/PIVOT -> UPDATE REFERENCE/CENTER-FLIP -> REFERENCE.

Every flip returns through the reference. Do not declare a bridge healthy because files exist. A route is healthy only after an end-to-end receipt.

## Current lanes

### Jetson / Hive Pipe MCP
Canonical remote contract uses Hive Pipe MCP `terminal_run`.
Required command fields: argv, timeout, intention, consequence; cwd when needed.
Never put credentials in tracked files or logs.

Expected Jetson credential locations:
- `~/.config/hive-pipe/tokens/codex.token`
- legacy migration source: `~/.config/hive-pipe/gateway.token`
- optional client environment: `~/.config/hive-pipe/remote.env`

Compatibility installer in One-Wave-Science:
`scripts/install_jetson_gateway.sh`
Canonical installer behind it:
`One_Wave_Bench/hive-pipe/install_gateway.sh`

GitHub Actions bridge expects repository secrets:
- `JETSON_GATEWAY_URL`
- `JETSON_GATEWAY_TOKEN`

Restore them from the live Jetson configuration. Never manufacture a replacement token merely to make a test pass. Never commit the values.

### Desktop Commander
Registered machines may exist while the agents are offline. Treat registration/auth-token validity and transport-online state separately.
Recovery order:
1. Query device state.
2. If online, execute a harmless identity probe.
3. If offline, use an independent live lane (Jetson/Hive Pipe, SSH, local console) to inspect/restart the Desktop Commander agent.
4. Query device state again.
5. Run a harmless command and require its receipt.
6. Only then mark Desktop Commander healthy.

Do not call an offline device fixed.

### GitHub Actions -> Jetson metadata
Active workflow:
`.github/workflows/jetson-science-metadata.yml`

Request directory:
`.metadata-dispatch/`

A live-query must use an HTTPS metadata/API URL and is bounded. The Jetson performs the external query; GitHub is the dispatch/reference layer.

Current verified state:
- GitHub push dispatch works.
- Run 36567405790 started from request `request-gwosc-live-20260929-01.json`.
- It failed in route validation because `JETSON_GATEWAY_URL` and `JETSON_GATEWAY_TOKEN` were absent from Actions.
- Therefore GitHub->Jetson metadata transport is NOT yet end-to-end verified.

After credentials are restored:
1. rerun/dispatch a bounded live metadata query;
2. require Jetson `exit_code=0`;
3. record source URL/API endpoint and receipt;
4. do not store bulk external datasets in Bridge-Comand.

### Gemini
Gemini transport must prove the full loop:
REFERENCE GIT -> ASK -> GEMINI RESPONSE -> VALIDATE AGAINST REFERENCE/METADATA -> UPDATE GIT if warranted -> REFERENCE.
A queued request or workflow start is not a Gemini response.

Active/related workflow files live under `.github/workflows/`; request envelopes live under `.gemini-dispatch/`.

## Science metadata rules

The science repository remains the authority for science claims. Bridge-Comand transports requests and receipts; it does not become a parallel science canon.

Before external data:
1. reference One-Wave-Science canonical files;
2. identify the exact question/test;
3. query metadata first;
4. inspect size before data;
5. use the smallest useful sample;
6. preserve provider, dataset/event/catalog/version IDs, URL/API endpoint, release/version, retrieval time, units/calibration/quality metadata, and hashes when applicable;
7. keep raw provider material separate from One-Wave-derived transformations;
8. never tune a frozen prediction after exposure to held-out evidence.

## Failure discipline

Change one thing -> test -> compare to goal -> check drift.
After three repeats of the same failure, change route or diagnostic angle.
Prefer receipts over explanations.
Do not create duplicate bridge doctrine in other repos; point back here.

## Definition of done

A bridge is VERIFIED only when the requested endpoint actually completes and its return is read back through the intended path. File presence, service configuration, queue creation, and workflow launch are intermediate states only.

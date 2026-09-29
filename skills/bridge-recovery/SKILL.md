# Bridge Recovery Skill

Use this skill whenever a One-Wave remote bridge, Jetson route, Desktop Commander connection, metadata worker, or AI relay is broken or uncertain.

## Mandatory loop
1. REFERENCE: read the canonical Bridge-Comand runbook and the target workflow/script before acting.
2. OBSERVE: obtain live state (device status, workflow run, job log, service receipt). Do not infer health from configuration.
3. LOCATE: name the first failing boundary.
4. REPAIR ONE BOUNDARY: make the smallest change that can advance the route.
5. VERIFY: execute a harmless end-to-end probe and read the returned receipt.
6. CENTER-FLIP: return to repo/reference and compare the observed result with the intended contract.
7. UPDATE: record durable non-secret recovery knowledge in Bridge-Comand. Never commit credentials.
8. REPEAT until the actual requested endpoint responds.

## Credential recovery
For Jetson Hive Pipe, inspect live host configuration in this order:
- ~/.config/hive-pipe/remote.env
- ~/.config/hive-pipe/tokens/codex.token
- ~/.config/hive-pipe/gateway.token (legacy)
- active gateway/cloudflared service configuration and logs for the current public URL.

GitHub Actions requires JETSON_GATEWAY_URL and JETSON_GATEWAY_TOKEN. Restore secret values through an authorized secret-management path; do not print them or commit them.

## Desktop Commander
If device is offline, do not retry the same remote command. Switch to another live lane and restart/repair the agent from the host side. Verification requires online status plus a successful harmless command receipt.

## Evidence rule
queued != running != completed != successful != end-to-end verified.
State exactly which one is proven.

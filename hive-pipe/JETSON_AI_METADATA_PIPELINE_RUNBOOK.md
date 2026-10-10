# Jetson AI Metadata Pipeline — Operations and Recovery

Status: **PARTIAL** as of 2026-10-10. Do not report the stable Tailscale HTTPS route as verified until a real GitHub Actions command returns a matching Jetson receipt.

## Authority and ownership
- Bridge authority: `One-Wave-Universe/Bridge-Comand` — start with `BRIDGE_COMMAND_START_HERE.md` and `hive-pipe/BRIDGE_DIRECTIONS.md`.
- Science authority: `One-Wave-Universe/One-Wave-Science`; canonical local checkout `/home/Scales/One-Wave-Science`.
- Keep provider metadata/raw responses and provenance separate from One-Wave hypotheses, transformations, and claims. No simulated data may be labeled real.
- The Jetson is NVIDIA Jetson Orin Nano Developer Kit Super, Linux ARM64 (`aarch64`), account `Scales`. The remote host name has been `localhost.localdomain`.
- No credentials, private keys, bearer tokens, or secret values in this repository or logs.

## Working local Hive Pipe
- Canonical service source: `/home/Scales/Bridge-Comand/hive-pipe/`.
- User services: `hive-pipe-agent.service` and `hive-pipe-gateway.service`. They are **user-level** systemd services, not system services. Query with `XDG_RUNTIME_DIR=/run/user/2002 systemctl --user status hive-pipe-agent.service hive-pipe-gateway.service` as Scales. A system-wide `systemctl is-active` may misleadingly say inactive.
- Gateway listens only on `127.0.0.1:8765`, MCP at `/mcp`, requiring a client token. Unauthenticated GET returning HTTP 401 is expected, not a failure.
- Queue watcher uses `hive-pipe/agent.sh --watch`.
- Canonical diagnostic: `cd /home/Scales/Bridge-Comand && python3 hive-pipe/bridge_doctor.py --profile all --json`. On 2026-10-10 it returned 7 PASS and exit 0, including authenticated local MCP command receipt `BRIDGE_DOCTOR_GATEWAY_OK` and reachable primary/backup pull branches.
- The authoritative health rule is an end-to-end command receipt, not just active processes.

## GitHub control plane — previously VERIFIED with Cloudflare quick tunnel
- GitHub repositories **each have their own Actions secrets**: `JETSON_GATEWAY_URL`, `JETSON_GATEWAY_TOKEN`. A secret set in Bridge-Comand does not propagate to One-Wave-Science.
- `One-Wave-Universe/Bridge-Comand`: `Jetson Science Metadata` workflow run `38037837444` succeeded and returned metadata listing from `/home/Scales/One-Wave-Science/.one-wave-metadata/`, Jetson exit 0.
- `One-Wave-Universe/One-Wave-Science`: `Jetson Command Lane` workflow run `38038123883` succeeded after its separate URL secret was updated; `hostname` returned `localhost.localdomain`, exit 0, cwd `/home/Scales/One-Wave-Science`.
- Those tests used a **temporary** Cloudflare `trycloudflare.com` quick tunnel. The hostname can change; discover its current value from the live `hive-pipe-cloudflared.service` output and reverify before updating secrets. Do not rely on a saved old URL.
- Never replace a working GitHub secret until the replacement endpoint is externally verified with an authenticated MCP receipt.
- GitHub Actions commands must supply `argv`, `cwd`, `timeout`, `intention`, `consequence` to the Hive Pipe `terminal_run` contract. Keep privileged operations outside the sandbox unless separately authorized through a legitimate administrator connection.

## Rootless Tailscale attempt — installed, joined, HTTPS not verified
- User confirmed phone and Dell laptop on same tailnet. Jetson Tailscale client reported online as `localhost-0` with tailnet IPv4 `100.101.231.90`; the laptop was `scales-latitude-e7450` and phone `vl68-pro`. This private IP is not a GitHub-hosted runner's public endpoint.
- Official Tailscale ARM64 archive version 1.104.1 was downloaded to Jetson, SHA256 `f60294374967f3dfd8cf57bbbd474d6cfce32d123e3a8ddeab82a87940daa806` verified at download time.
- Installed user-local under `/home/Scales/.local/share/one-wave-tailscale/tailscale_1.104.1_arm64/` (executables `tailscale`, `tailscaled`); socket `/home/Scales/.local/share/one-wave-tailscale/tailscaled.sock`, state `/home/Scales/.local/share/one-wave-tailscale/state`, state directory `/home/Scales/.local/share/one-wave-tailscale`.
- Rootless daemon invocation: `tailscaled --tun=userspace-networking --socket=SOCKET --state=STATE --statedir=STATE_DIR`, using those exact paths. Run as `Scales`, no sudo. The daemon was restarted with `--statedir` to address `no TailscaleVarRoot` from `tailscale cert`.
- CLI must use `tailscale --socket=SOCKET ...`; `tailscale up` authenticated the Jetson and `tailscale status` listed the tailnet devices.
- User enabled Funnel in the Tailscale admin UI. `tailscale funnel status` reported `https://localhost-0.tailc05a35.ts.net` proxying `http://127.0.0.1:8765`.
- **BLOCKER**: `curl https://localhost-0.tailc05a35.ts.net/mcp` from Jetson returned DNS resolution failure (`Could not resolve host`, HTTP 000), including after daemon restart. Funnel config alone is not proof of external reachability. `tailscale cert` was retried after setting `--statedir`, but certificate issuance completion was not confirmed.
- Rootless installation experiment script exists on branch `feature/jetson-rootless-tailscale-path`: `hive-pipe/rootless_tailscale.sh`. Its content is not yet merged or accepted as a complete persistent service.
- Tailscale user-level daemon persistence across logout/reboot has **not** been verified; do not assert permanent availability.
- Keep the Cloudflare tunnel active until DNS, HTTPS certificate, external authenticated MCP receipt, GitHub run, and reboot persistence all pass.

## Next smallest verification (no guesswork)
1. Verify Jetson identity, user service states, and local doctor.
2. Check `tailscale --socket=SOCKET status`, `funnel status`, and whether the rootless daemon is still running.
3. Query public DNS for the Funnel hostname **from an external resolver/network**. Check HTTPS TLS and an unauthenticated 401 response; if missing, investigate Tailscale Funnel certificate and tailnet settings. Do not paste credentials.
4. Perform a **bounded authenticated MCP command** through the public Funnel URL, with a unique request ID and expected stdout/exit code.
5. Only after #4 succeeds, update `JETSON_GATEWAY_URL` separately in Bridge-Comand and One-Wave-Science, leaving token values unchanged. Dispatch read-only GitHub workflows in both and inspect matching stdout/exit receipts.
6. Establish and test persistent user-level daemon startup, restart/reboot recovery, and rollback to Cloudflare. Then declare stable route VERIFIED.

## Metadata ingest acceptance
- Reference the exact Science nodes/chapters before requesting external data.
- Use provider's bounded public metadata API first; avoid unbounded bulk downloads.
- Record provider, instrument/event/catalog/version, source URL, retrieval UTC timestamp, units, calibration and quality flags where available, content hash, byte count, source class `real|simulated|test`, and request/receipt IDs.
- Raw provider data and its checksums stay immutable; derived interpretations are separate.
- `/home/Scales/One-Wave-Science/.one-wave-metadata/` is the proven metadata cache root. A file listing is **not** proof of a fresh ingest.
- Require the remote result to be read back through the requested path before promoting a job to VERIFIED or DONE.

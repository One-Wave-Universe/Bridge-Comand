---
name: bridge-control
description: Use the One-Wave Hive Pipe MCP tools to verify and repair the user's authorized bridge lattice and run bounded machine commands with receipts.
---

# Bridge control

Prefer `terminal_reference` then `terminal_pwd` before mutations when machine state is uncertain.
Use `terminal_run` for bounded argv execution and preserve its intention/consequence fields.
Treat stdout, stderr, exit code, and reference receipts as execution evidence.
Never claim a queued or repository change executed on a machine without a matching machine receipt.
When a route fails, check the bridge lattice watchdog and alternate public routes before asking the user to bootstrap anything.

Before cross-repo worker or machine handoffs, load `METADATA_AND_HANDOFF_CONTRACT.md` and preserve request IDs, canon references, provenance, source class, limits, and expected receipt type.
For Jetson Brain work, preserve FIELD/VOID/ROUTER role, backend, source tag, state hashes, budgets, and CPU/GPU parity fixture metadata.
Failures are receipts; after three equivalent failures switch route/angle rather than repeating blindly.

## Phone / Android route

Mobile clients use `PHONE_BRIDGE_PROFILE.md`. Do not assume localhost, SSH, inbound ports, persistent background execution, or a repo checkout on the phone. Preserve the same envelope/request ID through outbound HTTPS/durable queue to the machine receipt, with idempotent resume after suspension.

## Common device front door

Phone and laptop share the same GitHub→Actions→Jetson control plane. See `GITHUB_DEVICE_CONTROL_PLANE.md`. Local listeners, SSH, LAN access and Remote Desktop are optional accelerators/failovers, not prerequisites for originating a Jetson request.

## Device lattice

Load `DEVICE_LATTICE.md` for cross-device routing. Phone, laptop and Jetson are addressable lattice nodes through GitHub; preserve one request ID, provenance and chained hop receipts across every route. “Open” means authenticated/routable, never unauthenticated shell exposure.

## AI route discovery

AI agents: load `AI_ROUTING.md` first for device work and parse `ai-route-manifest.json` when a machine-readable route map is useful. Do not stop merely because one listener/route is unavailable; use the authorized lattice failover rules and require a matching final-target receipt.

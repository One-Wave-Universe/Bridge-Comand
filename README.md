# Bridge-Comand

Canonical One-Wave home for Hive Pipe, bridges, relays, terminal routing, Jetson access, AI adapters, recovery, receipts, and metadata transport.

Start with `BRIDGE_COMMAND.md`.

This is **not** the CELL hardware repo. Iron lives in `One-Wave-Universe/Builds`.

Rules:
- Do not claim a route is live without a matching execution receipt.
- "No direct terminal tool" is not a stop condition; try the next available bridge.
- Use intention + consequence for executable bridge actions.
- Keep credentials and tokens outside git.
- Do not duplicate bridge authority into Builds or Science.

## Shared metadata contract

All Foreman, worker, Jetson Brain, AI-adapter, simulator, and machine handoffs use the transport contract in `METADATA_AND_HANDOFF_CONTRACT.md`. JSON schemas live under `schemas/`.

Project semantics remain in the owning repo. Bridge-Comand owns transport envelopes, route evidence, provenance transport, and execution receipts.

## Phone / Android route

Mobile clients use `PHONE_BRIDGE_PROFILE.md`. Do not assume localhost, SSH, inbound ports, persistent background execution, or a repo checkout on the phone. Preserve the same envelope/request ID through outbound HTTPS/durable queue to the machine receipt, with idempotent resume after suspension.

## Preferred phone control plane

For immediate phone→Jetson commands, use GitHub as the public control plane: see `PHONE_GITHUB_JETSON.md` and `.github/workflows/jetson-command.yml`. The phone never needs the Jetson LAN address or gateway token.

## Common device front door

Phone and laptop share the same GitHub→Actions→Jetson control plane. See `GITHUB_DEVICE_CONTROL_PLANE.md`. Local listeners, SSH, LAN access and Remote Desktop are optional accelerators/failovers, not prerequisites for originating a Jetson request.

## Device lattice

Load `DEVICE_LATTICE.md` for cross-device routing. Phone, laptop and Jetson are addressable lattice nodes through GitHub; preserve one request ID, provenance and chained hop receipts across every route. “Open” means authenticated/routable, never unauthenticated shell exposure.

## AI route discovery

AI agents: load `AI_ROUTING.md` first for device work and parse `ai-route-manifest.json` when a machine-readable route map is useful. Do not stop merely because one listener/route is unavailable; use the authorized lattice failover rules and require a matching final-target receipt.

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

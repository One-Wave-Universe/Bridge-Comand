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

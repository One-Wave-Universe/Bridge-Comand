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

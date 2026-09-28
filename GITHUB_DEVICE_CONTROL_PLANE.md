# GitHub Device Control Plane

**Canonical front door for phone and laptop control of the Jetson.**

## Route

`PHONE OR LAPTOP → GITHUB → GITHUB ACTIONS → AUTHENTICATED HIVE PIPE GATEWAY → JETSON → ACTION LOG/RECEIPT → ORIGINATING DEVICE`

Phone and laptop use the same command semantics, security boundary, request IDs and receipt rules.

## Why

The originating device must not need:
- Jetson LAN access;
- SSH configuration;
- Jetson localhost access;
- a persistent local listener;
- a local repository checkout;
- the Jetson gateway token.

GitHub provides the durable device-independent control surface. Direct LAN, Remote Desktop Commander, pull bridge and other routes are optional accelerators/failovers, not prerequisites.

## Immediate command

Use **Actions → Jetson Command Lane → Run workflow**.

Provide a bounded argv JSON or simple command plus intention and consequence.

Safe smoke test:
`["uname","-a"]`

End-to-end success requires Jetson output and exit code in the Action log. A queued workflow or green non-machine validation is not a Jetson execution receipt.

## Device equivalence

A request created on phone and the equivalent request created on laptop must produce the same machine-side command semantics. UI/device differences must not change:
- argv;
- cwd;
- timeout;
- intention/consequence;
- permissions;
- assumption/transformation IDs;
- provenance;
- receipt requirements.

## Durable/deferred work

If immediate Jetson execution is unavailable, preserve the request through the store-and-forward contract with its stable ID. Later execution must return a receipt tied to that exact request ID.

## Security

GitHub secrets hold gateway credentials. Never commit or display tokens in request files, Action inputs, documentation, receipts or logs.

## Route policy

1. GitHub Device Control Plane is the common phone/laptop front door.
2. Direct routes may be used when demonstrably live.
3. A failed route is recorded and another route may be attempted.
4. Do not wait indefinitely for a listener.
5. After three equivalent failures, switch route/angle.
6. Only a matching machine receipt proves Jetson execution.

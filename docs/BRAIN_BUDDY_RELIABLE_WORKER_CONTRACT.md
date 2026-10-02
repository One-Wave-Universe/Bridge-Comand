# Brain Buddy Reliable Worker Contract

Status: recovery implementation gate

Brain Buddy must not depend on a provider being reached by one particular machine, bridge, phone, CLI, API, or browser session.

## Required invariant

A Council worker is READY only when it can accept the canonical Brain Buddy envelope and produce a matching durable receipt.

Every request carries:
- stable request_id
- Baseline Zero/reference state
- Weight of Time/session state
- task
- required capabilities
- allowed side effects
- acceptance test

Every return carries:
- same request_id
- worker/provider identity
- transport actually used
- referenced state
- answer/result
- validation status
- explicit failure when unsuccessful

Queued or dispatched is never PASS. Only a matching returned receipt is PASS.

## Worker generations

Provider behavior is adapter-specific. Do not force DeepSeek and Gemini through identical transports.

Gemini currently has a proven GitHub-native provider route.

DeepSeek may use a logged-in web-session worker/relay. Its browser/session authentication remains outside the repository. The worker exposes only the bounded Brain Buddy adapter contract.

New provider workers may be added without changing Council semantics.

## Reliability lattice

For each provider, maintain ordered authorized routes:
1. healthy primary worker
2. healthy alternate worker/transport
3. optional machine-local worker when local capability is actually required

Route health is explicit. A failed route is quarantined/backed off; the same request_id may be delivered to an alternate route, but results are deduplicated by request_id.

Never silently convert a provider failure into a different provider's answer.

## Device role

The phone is simply another place to work from, alongside the laptop, Jetson, Chromebook, or another authorized device. It is not a special controller and no device owns Brain Buddy.

Any authorized device may enter the same persistent Brain Buddy session to submit work, redirect discussion, inspect state, admit results, continue Council work, or perform capabilities available on that device.

Changing, disconnecting, or replacing a device must not lose Council state, Baseline Zero, Weight of Time, pending work, or receipts.

No persistent repository clone is required on the phone or laptop. Device-specific bridges are transport adapters only; they do not define Council authority or session ownership.

## Persistence and recovery

Durable state must preserve:
- current Baseline Zero
- Weight of Time
- admitted and pending VIEWs
- request IDs and their phases
- worker health
- returned receipts
- unresolved contradictions
- branch/checkpoint lineage

Restart behavior:
1. reload durable session
2. re-reference current Baseline Zero
3. reconcile pending request IDs
4. do not repeat an execution whose completion is uncertain
5. retry/fail over only when safe
6. continue Council from preserved Weight of Time

## Always-works gate

Do not call Brain Buddy reliable merely because it worked once.

PASS requires repeated tests of:
- clean startup
- Gemini return
- DeepSeek return
- parallel Council return
- back-and-forth Weight-of-Time continuation
- provider worker restart
- Brain Buddy restart
- one route failure with authorized failover
- duplicate request suppression
- stale/late result admission
- device disconnect and reconnect
- missing provider isolation (other workers continue)
- no laptop internal-disk repo replication
- branch-safe repo update
- rollback to known-good checkpoint

Each test must leave an observable matching receipt. Any failure remains a failed test, not a partial PASS.

## Development law

KNOWN-GOOD -> NEW RECOVERY/GOAL BRANCH -> BUILD -> TEST -> PASS -> CHECKPOINT -> NEXT BRANCH

Do not promote this reliability work to main until the full gate repeatedly passes.

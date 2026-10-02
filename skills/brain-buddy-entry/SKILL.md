# Brain Buddy Entry Skill

## Purpose
This is the mandatory entry plugin/skill for ChatGPT and every other Brain Buddy-capable AI. It exists to stop workers from choosing a convenient tool or machine before loading Brain Buddy routing authority.

## Hard start rule
For any One-Wave / Brain Buddy / Science / repo / bridge / worker task:

1. ENTER BRAIN BUDDY FIRST.
2. Load the current Brain Buddy Baseline Zero / shared-state manifest.
3. Load Bridge-Comand routing/reference authority before selecting any execution path.
4. Identify the owning repo, current branch/checkpoint, and exact task.
5. Resolve the route from repo-declared capabilities and known-good receipts.
6. Only then invoke GitHub, provider bridges, Hive Pipe, Jetson, Desktop Commander, phone bridge, API, CLI, or another transport.

DO NOT start from whichever tool is easiest to call.

## Route precedence
Use evidence, not a permanently hard-coded machine order.

For recovery:
LAST REAL SUCCESS RECEIPT -> exact route/worker -> exact branch/commit -> restore/test same packet -> only then fail over.

For new work:
Brain Buddy shared state -> owning repo authority -> route manifest/skills -> healthy authorized capability -> execute -> matching receipt.

Desktop Commander is not a default Brain Buddy route. It is used only when the current Brain Buddy route state explicitly selects it or a bounded recovery task requires direct machine inspection.

Jetson is primarily bridge/worker infrastructure, metadata pipeline access, and machine-local evidence. Do not assume a Jetson task merely because a bridge once ran there.

## Mandatory preflight
Before acting, the worker must be able to state internally:
- Brain Buddy session/baseline being used
- owning repo
- governing reference/routing files
- known-good checkpoint
- selected capability/route and why
- required proof of success

If any item is unknown, retrieve it from the repo/shared state. Do not guess.

## Recovery law
A broken current route does not prove the provider is broken.
A missing process on one machine does not prove the route no longer exists.
Queued/dispatched is not executed.
A worker is live only after a matching real return receipt.

## Completion
Write material route discoveries, corrections, and known-good receipts back into Brain Buddy shared state so the next AI/device begins from the corrected Baseline Zero.

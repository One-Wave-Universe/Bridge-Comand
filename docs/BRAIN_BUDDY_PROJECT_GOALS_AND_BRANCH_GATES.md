# Brain Buddy Project Goals and Branch Gates

## Non-negotiable purpose

Build a durable Brain Buddy system in which multiple AI workers can collaborate on One-Wave science and coding while preserving known-good architecture at every development step.

A working architecture MUST NEVER be overwritten merely to try the next idea.

## Absolute branch law

Every substantial goal below is developed on a NEW CHILD BRANCH created from the last proven checkpoint.

Pattern:

`KNOWN-GOOD CHECKPOINT -> NEW GOAL BRANCH -> BUILD -> TEST -> PASS -> CHECKPOINT -> NEXT CHILD BRANCH`

If a goal fails:

`KNOWN-GOOD CHECKPOINT -> FAILED EXPERIMENT BRANCH`

The failed branch remains isolated. Return to the known-good checkpoint and try a different child branch.

Rules:
1. Never experiment directly on `main`.
2. Never use the current working branch as a scratchpad for the next substantial architecture change.
3. One substantial architecture evolution per branch.
4. Commit a working checkpoint before creating the next evolution branch.
5. Never delete the last known-good state merely because a newer branch exists.
6. Never merge a failing or partially understood evolution into a known-good branch.
7. A queued request, mocked result, or process start is not proof of success.
8. Promotion requires repeatable tests and real receipts/results where external workers are involved.
9. `main` is promoted only after an intentionally selected integrated version is solid.
10. After promotion, the exact canonical commit becomes the new development Baseline Zero.

## Current architecture preservation point

Current architecture work is being defined on:

`architecture/brain-buddy-science-baseline-loop-20261001`

Before implementation work expands, preserve this architecture branch as the parent/reference specification. Implementation goals branch FROM a proven implementation checkpoint; architecture documentation does not authorize destructive edits to an older working implementation.

---

# BUILD GOALS

## GOAL 00 — Preserve and inventory known-good behavior

### Purpose
Identify exactly what already works before changing execution code.

### New branch
Create a dedicated inventory/recovery branch from the strongest known-good Brain Buddy implementation.

### Must deliver
- exact known-good commit SHA;
- runnable entrypoints;
- existing Gemini route behavior;
- existing DeepSeek route behavior;
- Council behavior;
- known authentication requirements;
- known failures;
- restart behavior;
- files/services/workflows required;
- a minimal repeatable smoke test.

### Must NOT
- redesign loops;
- replace provider routes;
- clean up working code merely for style;
- modify Science canon;
- declare broken external execution successful.

### PASS
A fresh invocation reproduces the documented known-good behavior.

### Checkpoint
Create/retain an explicit known-good checkpoint before Goal 01.

---

## GOAL 01 — Freeze core contracts and state schemas

### Purpose
Separate Brain Buddy logic from AI providers, transports and UI.

### New branch
Child of Goal 00 checkpoint.

### Deliver
Schemas/contracts for:
- session;
- event;
- worker identity/capabilities;
- provider adapter;
- transport adapter;
- request/result/receipt;
- Baseline Zero reference;
- Weight of Time;
- loop admission/participation;
- failure/block state.

### Must NOT
- require Gemini/DeepSeek to prove schema;
- replace working bridges yet;
- add GUI.

### PASS
Fake workers using fake transports can execute the contracts without provider-specific code in the core.

### Checkpoint
`contracts-v1` known-good state.

---

## GOAL 02 — Persistent headless Brain Buddy engine

### Purpose
Make the Council survive process/app restarts.

### New branch
Child of Goal 01 checkpoint.

### Deliver
- create session;
- resume session;
- durable event/state store;
- worker registry;
- asynchronous jobs;
- pending/completed/failed distinction;
- restart recovery;
- no fabricated completion.

### Must NOT
- require GUI;
- alter Weight-of-Time semantics;
- directly edit canonical Science.

### PASS
Kill the engine with work pending, restart it, and recover the correct state repeatedly.

### Checkpoint
`persistent-engine-v1`.

---

## GOAL 03 — Provider adapter boundary

### Purpose
Make AI providers replaceable/addable without changing Council logic.

### New branch
Child of Goal 02 checkpoint.

### Deliver common capabilities
`ask / continue / observe / status / cancel / receipt / capabilities`

### First adapters
- Gemini;
- DeepSeek;
- existing/local ChatGPT-facing route where authorized;
- mock adapter for deterministic tests.

### Must NOT
- hard-code Jetson as Gemini;
- treat authentication failure as model failure;
- fabricate external responses;
- rewrite Council logic for each provider.

### PASS
Core runs unchanged when adapters are swapped, unavailable, delayed or failed.

### Checkpoint
`provider-adapters-v1`.

---

## GOAL 04 — Transport lattice

### Purpose
Separate model/provider from how Brain Buddy reaches it.

### New branch
Child of Goal 03 checkpoint.

### Required transport classes
Implement as needed while preserving interfaces:
- GitHub/control-plane;
- local subprocess/stdin/stdout;
- HTTP/HTTPS;
- streaming/WebSocket where useful;
- filesystem/queue watcher;
- Linux/Jetson SSH and service control;
- Windows PowerShell/PowerShell Remoting or other authorized Windows route;
- MCP/plugin/app connector;
- vendor CLI/API;
- future container/message-bus/remote-worker route.

### Must NOT
- make any single transport globally mandatory;
- redesign Brain Buddy when a route changes;
- assume machine type before capability discovery.

### PASS
Equivalent request envelopes can travel through at least two transports and return normalized results.

### Checkpoint
`transport-lattice-v1`.

---

## GOAL 05 — Executable Weight of Time v1

### Purpose
Turn Weight of Time from documentation into persistent engine behavior.

### New branch
Child of Goal 04 checkpoint.

### Carry forward
- competing views;
- material disagreements;
- unresolved contradictions;
- attempted derivations/tests;
- evidence gained;
- evidence missing;
- rejected/failed paths and reasons;
- claim/gate state;
- material worker contributions;
- Baseline Zero lineage.

### Core law
Weight is accumulated unresolved consequence/history, NOT merely elapsed wall-clock time, a timeout, or a fixed round counter.

### Must NOT
- erase unresolved history at restart;
- erase unresolved history at commit;
- force synchronized rounds;
- equate consensus with truth.

### PASS
A new worker after restart can continue the unresolved problem from compressed Weight-of-Time state without replaying the entire transcript.

### Checkpoint
`weight-of-time-v1`.

---

## GOAL 06 — Back-and-forth best-answer loop

### Purpose
Make the original Weight-of-Time dialogue operational.

### New branch
Child of Goal 05 checkpoint.

### Behavior
- workers run asynchronously;
- available workers continue while others think;
- returned result becomes a new VIEW;
- workers may challenge/research/re-reference;
- materially improved state goes back through workers;
- late results are admitted as new views;
- no provider owns the clock;
- no fixed mandatory round count.

### Settlement
Settle only when current validation is satisfied and remaining uncertainty is explicitly carried forward.

### PASS tests
- Gemini first / DeepSeek late;
- DeepSeek first / Gemini late;
- one provider fails;
- provider changes conclusion;
- late evidence contradicts current answer;
- restart mid-discussion.

### Checkpoint
`weight-of-time-dialogue-v1`.

---

## GOAL 07 — One-Wave reference bundle

### Purpose
Give every science worker the same authoritative starting state.

### New branch
Child of Goal 06 checkpoint.

### Reference order
1. current Baseline Zero;
2. One-Wave lens/canonical start;
3. logic/reference rules;
4. exact relevant nodes;
5. exact relevant chapters;
6. read-only Jetson pipeline metadata;
7. external/public evidence as needed;
8. current inherited Weight of Time.

### Jetson metadata law
CERN/LIGO/other pipeline data and Wave-transformed numeric outputs are READ-ONLY evidence to the Council. Record exact source/pipeline/transform/version/hash. Do not hand-edit those outputs during science discussion.

### PASS
Two workers receive reproducible reference bundles pointing to the same baseline and evidence versions.

### Checkpoint
`science-reference-v1`.

---

## GOAL 08 — Bounded One-Wave Science Room

### Purpose
Run one complete science problem through Brain Buddy before broad autonomy.

### New branch
Child of Goal 07 checkpoint.

### Complete loop
`BASELINE ZERO -> REFERENCE -> COUNCIL -> WEIGHT OF TIME -> VALIDATE -> PROPOSE BRANCH EDITS -> RE-REFERENCE`

### Writable outputs
- affected science nodes;
- affected chapters;
- writable claim/gate/provenance/reference records.

### Read-only inputs
- CERN/LIGO/other source/pipeline metadata outputs.

### Must NOT
- write directly to Science main;
- silently update a node without affected chapter;
- silently update a chapter without governing node;
- turn hypothesis into established result without evidence.

### PASS
One bounded science problem produces a coherent reviewable Science branch with provenance and unresolved weight intact.

### Checkpoint
`science-room-v1`.

---

## GOAL 09 — Baseline Zero update/re-reference cycle

### Purpose
Make accepted repo evolution feed back into every continuing AI.

### New branch
Child of Goal 08 checkpoint.

### Behavior
After an accepted canonical Science commit:
- record exact new Baseline Zero SHA;
- invalidate stale reference bundles;
- rebuild affected references;
- preserve unresolved Weight of Time;
- force continuing workers to re-reference before downstream reasoning.

### PASS
A worker holding stale pre-update context cannot continue as though it outranks the new baseline.

### Checkpoint
`baseline-rereference-v1`.

---

## GOAL 10 — Brain Buddy App

### Purpose
Create the human-facing Science/Council application without moving core logic into the UI.

### New branch
Child of Goal 09 checkpoint.

### Views
- session/Council;
- worker state;
- live dialogue;
- WATCH/LISTEN/THINK;
- Weight of Time;
- references/evidence;
- proposed repo edits;
- Baseline Zero lineage;
- transport/bridge health.

### Must NOT
- make closing the GUI terminate Council state;
- duplicate engine logic in UI;
- make GUI the only usable interface.

### PASS
GUI and headless/CLI clients reconnect to the same live session.

### Checkpoint
`brain-buddy-app-v1`.

---

## GOAL 11 — Coding Workbench

### Purpose
Let multiple AIs code together without destroying working code.

### New branch
Child of Goal 10 or the appropriate stable engine checkpoint.

### Behavior
- each substantial coding evolution gets isolated branch/worktree;
- AI workers may build/test/review;
- worker-to-worker review;
- known-good checkpoint retained;
- integration candidate assembled separately;
- no direct main edits.

### Program bridges
Add whatever authorized capability is required:
- shell;
- PowerShell;
- compiler/build tools;
- test runners;
- containers;
- GitHub;
- IDE/agent interfaces;
- remote machines.

### PASS
At least two workers can independently modify/test isolated work and produce a reviewable integration candidate without collision.

### Checkpoint
`coding-workbench-v1`.

---

## GOAL 12 — Persistent project loops

### Purpose
Allow separate projects to develop independently without one giant context.

### New branch
Child of stable Brain Buddy engine.

### Each project owns
- Baseline Zero;
- Weight of Time;
- participants;
- authority;
- references;
- current problems/work;
- branch lineage.

### PASS
Two project loops survive restart and evolve independently.

### Checkpoint
`project-loops-v1`.

---

## GOAL 13 — Cross-project Council

### Purpose
Let project loops convene and compare without collapsing authority boundaries.

### New branch
Child of Goal 12 checkpoint.

### Exchange
- current baseline;
- discoveries;
- unresolved weight;
- contradictions;
- dependencies;
- requests for expertise.

Findings return to owning project loops as proposals.

### Must NOT
Allow one project Council to silently rewrite another project's canon.

### PASS
A cross-project finding returns to the owning project, is independently validated there, and either accepted or rejected with lineage preserved.

### Checkpoint
`cross-project-council-v1`.

---

## GOAL 14 — Voluntary AI cross-loop mobility

### Purpose
Allow an AI to notice another relevant loop and ask to enter.

### New branch
Child of Goal 13 checkpoint.

### Protocol
`REQUEST-ENTRY -> ADMIT | DEFER | DECLINE`

Default admitted state:

`WATCH -> LISTEN -> THINK`

Only after understanding the target loop may the worker request:
- `REQUEST-SPEAK`;
- `REQUEST-WORK`;
- `REQUEST-REVIEW`.

### Must re-reference
- target Baseline Zero;
- target rules/lens;
- relevant state;
- inherited Weight of Time.

### PASS
An observing worker can enter and understand another loop without editing, redirecting or interrupting it, then make a controlled participation request.

### Checkpoint
`cross-loop-mobility-v1`.

---

## GOAL 15 — Expanded Weight of Time / nested Councils

### Purpose
Carry Weight of Time across workers, sessions, project loops and convening Councils.

### New branch
Child of Goal 14 checkpoint.

### Develop
- local problem weight;
- project-level weight;
- cross-project weight;
- compression without erasure;
- lineage between baseline changes;
- reopening when new evidence materially changes a settled path;
- selective context reconstruction for new workers.

### PASS
A later Council can reconstruct why an unresolved issue exists, which evidence changed it, and which project owns the next action without loading all historical transcripts.

### Checkpoint
`nested-weight-of-time-v1`.

---

# MAIN PROMOTION GATE

Do NOT promote an integrated Brain Buddy version to `main` merely because all features exist.

A candidate main must demonstrate:
- repeatable startup;
- repeatable restart/recovery;
- provider failure isolation;
- transport failure isolation/failover where authorized;
- real external worker receipts;
- persistent Weight of Time;
- correct Baseline Zero re-reference;
- branch-safe repo updates;
- no mutation of read-only science pipeline metadata;
- known-good rollback point;
- documented install/run/recovery procedure;
- Science Room bounded test;
- coding Workbench bounded test if included in that release.

Only after those gates pass is a deliberate main promotion considered.

After promotion:
`MAIN COMMIT = NEW DEVELOPMENT BASELINE ZERO`

Every later substantial evolution starts from a child branch again.

# Project completion definition

The project is not “done” when multiple AIs can chat.

The intended mature system is one where:
- AIs can work asynchronously and carry Weight of Time;
- One-Wave science can reference canon, logic, Jetson numeric metadata and external evidence;
- validated science changes coherently update branch copies of nodes/chapters/reference records;
- accepted commits establish new shared Baseline Zeros;
- all workers re-reference rather than drifting;
- coding workers operate in isolated branches/worktrees;
- independent project loops can convene;
- AIs can voluntarily request entry, observe first, then participate;
- provider and machine bridges can evolve without replacing the Brain Buddy architecture;
- every major evolution preserves a known-good return point.

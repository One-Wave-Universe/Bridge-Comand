# Brain Buddy Planned Build Strategy

## Goal

Build Brain Buddy as a persistent multi-AI collaboration system for One-Wave science and coding work. Design from required capabilities outward. Do not constrain the architecture to transports, programs, providers, machines or credentials that happen to be available today.

The system has one durable core and multiple surfaces:
- Science Room;
- Coding Workbench;
- GUI app;
- headless program/service;
- future project Councils and cross-project convening.

All substantial development remains branch-first until a repeatedly tested solid version is deliberately promoted.

## Architectural separation

### 1. Brain Buddy core
Owns sessions, workers, Weight of Time, loop state, admission, interrupts, Baseline Zero references, task state and receipts. It must not know whether a worker was reached through HTTP, PowerShell, SSH, a CLI, MCP, GitHub or another transport.

### 2. Provider adapters
One adapter per AI/provider. Common conceptual contract:
`ask / continue / observe / status / cancel / receipt / capabilities`.

Examples: ChatGPT, Gemini, DeepSeek, Claude, Grok, local models and future providers.

### 3. Transport adapters
Move requests/results between Brain Buddy and programs/machines. Required transport classes should be implemented as needed rather than treated as architecture:
- HTTP/HTTPS and streaming/WebSocket;
- local subprocess/stdin/stdout;
- filesystem/queue watcher;
- GitHub control plane/workflows;
- SSH for authorized Unix/Linux machines;
- systemd/service control on Linux/Jetson;
- PowerShell/PowerShell Remoting or another authorized Windows control route;
- MCP/plugin/app connectors;
- browser or vendor CLI/API routes where appropriate;
- later message bus/container/remote-worker transports.

No single transport is mandatory for all workers.

### 4. Repository/reference layer
Resolves owning repo, Baseline Zero, One-Wave lens/canon, nodes, chapters, reference rules, writable claim/reference records and branch state.

### 5. Evidence/data layer
Read-only access to Jetson CERN/LIGO/other numeric metadata pipelines and Wave-transformed outputs, plus external/public evidence. Preserve source, transform, version/hash and provenance. Science discussion does not hand-edit pipeline outputs.

## Development phases

### Phase 0 — Freeze requirements and contracts
Deliver:
- canonical state-machine vocabulary;
- worker/provider contract;
- transport contract;
- session envelope;
- Weight-of-Time state schema;
- Baseline Zero/reference schema;
- receipt/result schema;
- capability discovery schema.

Test: a fake worker and fake transport can exercise the contracts without Gemini, DeepSeek, Jetson or internet access.

Gate: contracts are independent of provider and machine.

### Phase 1 — Persistent single-machine Brain Buddy engine
Build a headless service first.

Deliver:
- create/resume session;
- durable event log/state;
- worker registry;
- asynchronous task execution;
- WATCH/LISTEN/THINK;
- REQUEST-SPEAK / REQUEST-WORK / REQUEST-REVIEW;
- interrupt/defer/admit behavior;
- restart recovery;
- Weight of Time persisted separately from raw transcript.

Test: kill/restart service during multiple fake-worker tasks and recover exact state without inventing completed work.

Gate: repeated restart/recovery tests pass.

### Phase 2 — Real provider adapter framework
Move existing Gemini and DeepSeek routes behind the common adapter contract, then add other providers without modifying the core.

Deliver:
- capability detection;
- authentication state reported explicitly;
- streaming or polling normalized to events;
- stable request IDs;
- real return receipts;
- failure classification;
- route failover without fabricated success.

Test: substitute mock adapters, live adapters and unavailable adapters in the same session.

Gate: provider failure cannot corrupt Council state.

### Phase 3 — Transport lattice
Implement transports as interchangeable routes.

Start with the routes most useful for current machines, but retain the full interface:
- GitHub;
- local process;
- HTTP;
- Linux/Jetson SSH/service route;
- Windows PowerShell route when Windows program control is required;
- filesystem watcher/queue;
- MCP/plugin routes.

Add capability discovery so Brain Buddy asks what a node can do instead of assuming a machine type.

Test: send the same worker envelope through two different transports and receive equivalent normalized results.

Gate: loss of one route permits authorized failover without changing the science/coding loop.

### Phase 4 — Weight of Time v1
Implement Weight of Time as executable state, not documentation.

Carry:
- competing views;
- unresolved contradictions;
- attempted derivations/tests;
- evidence gained/missing;
- rejected paths and reasons;
- claim/gate state;
- material worker contributions;
- Baseline Zero lineage.

Do not equate weight with elapsed wall-clock time or fixed rounds.

Test: resume a problem after restart/new worker and verify it can continue from compressed unresolved state without replaying the entire transcript.

Gate: new evidence can reopen a previously settled-looking path without losing lineage.

### Phase 5 — One-Wave Science Room
Implement the science loop:

`Baseline Zero -> One-Wave lens/canon -> logic/reference rules -> nodes/chapters -> READ Jetson metadata -> external evidence -> Council/Weight of Time -> validate -> branch updates to nodes/chapters/claim-reference records -> candidate new Baseline Zero -> re-reference workers`.

Deliver:
- read-only metadata connector;
- internet/evidence connector;
- reference bundle builder;
- proposed edit bundle;
- node/chapter consistency checker;
- provenance/evidence links;
- branch-only Science updates.

Test with one bounded One-Wave problem before broad autonomous science work.

Gate: no stale node/chapter pair and no pipeline metadata mutation.

### Phase 6 — Back-and-forth best-answer loop
Make the Weight-of-Time dialogue operational.

Workers return asynchronously. Available workers continue. A new result becomes a new VIEW. Material disagreement/evidence can trigger another pass. No provider owns the clock and there is no mandatory fixed round count.

Add settlement criteria based on resolved work, validation and remaining material uncertainty rather than simple consensus.

Test adversarially with workers returning in different orders, one failing, one changing its conclusion, and late contradictory evidence.

Gate: final state records both settled result and unresolved weight.

### Phase 7 — Science Baseline Zero promotion loop
Generate coherent branch edits to affected nodes, chapters and writable claim/reference records. Validate before proposing promotion.

After an accepted canonical commit:
- mark exact commit as new Baseline Zero;
- invalidate stale reference bundles;
- re-reference every continuing worker;
- carry unresolved Weight of Time forward.

Gate: no worker continues downstream as if its stale pre-commit context outranks the new baseline.

### Phase 8 — Brain Buddy App
Build GUI on top of the service, not instead of it.

Views:
- Council/session;
- worker status;
- live discussion;
- WATCH/LISTEN/THINK observers;
- Weight of Time;
- evidence/references;
- proposed repo changes;
- Baseline Zero lineage;
- route/bridge health.

Closing the GUI must not destroy Council state.

Gate: CLI/headless and GUI operate the same session.

### Phase 9 — Coding Workbench
Use the same engine with coding-specific authority.

Deliver:
- isolated branch/worktree per substantial worker task;
- code/test/review loops;
- worker-to-worker review;
- build/test receipts;
- known-good checkpoints;
- no direct main edits;
- deliberate promotion.

Add program bridges required by target environments: shell, PowerShell, compilers, IDE/agent interfaces, containers, test runners, GitHub and remote machines.

Gate: two or more workers can modify/test isolated work without colliding, then produce a reviewable integration candidate.

### Phase 10 — Multiple persistent project loops
Each project owns:
- its Baseline Zero;
- local Weight of Time;
- participants;
- references;
- authority boundaries;
- current work.

Project loops run independently rather than sharing one giant context.

Gate: projects can continue independently through restart and update cycles.

### Phase 11 — Cross-project Council
Projects convene using compressed project state.

Exchange:
- baseline;
- relevant discoveries;
- unresolved weight;
- contradictions;
- dependencies;
- requests for expertise.

Cross-project findings return to the owning loop as proposals. One project never silently rewrites another project's canon.

Gate: cross-project exchange cannot bypass project authority.

### Phase 12 — Voluntary AI mobility
Workers may REQUEST-ENTRY into another loop.

Default admitted state:
`WATCH -> LISTEN -> THINK`.

Only afterward may a worker request SPEAK, WORK or REVIEW. It first re-references the target Baseline Zero and inherited Weight of Time.

Later add specialist borrowing and temporary Councils.

Gate: observer entry causes no edits or unsolicited control changes.

## Bridge/program capability map

Brain Buddy should eventually be able to bridge to capabilities, not brands:

| Capability | Candidate mechanisms |
|---|---|
| Git/repository | Git CLI, GitHub API/plugin, workflows |
| Linux/Jetson process/service | local shell, SSH, systemd |
| Windows process/service | PowerShell, PowerShell Remoting/WinRM, SSH where configured |
| AI provider | official API/SDK, authorized CLI, MCP/plugin, browser-capable adapter where permitted |
| Local AI | subprocess/API server/container |
| Files/watchers | filesystem API, queue directories, watcher service |
| Build/test | subprocess, container, CI workflow, remote worker |
| Science metadata | read-only pipeline/query adapters |
| Internet evidence | research/search adapters with source provenance |
| Long-running events | event stream/message bus/queue |
| GUI | local/web/desktop client talking to Brain Buddy service |

Mechanisms are replaceable. The capability contract is the durable interface.

## Branch strategy

1. Never develop experimental Brain Buddy work directly on main.
2. One substantial evolution per explicit branch.
3. Test and checkpoint a working state before branching into the next substantial evolution.
4. Preserve known-good branches/tags until replacement is proven.
5. Failed experiments stay isolated.
6. Promotion to a solid main version is deliberate and evidence-based.
7. After promotion, that commit becomes the new development Baseline Zero.

## Immediate build order

Do not attempt all phases at once.

First implementation sequence:
1. contracts/state schemas;
2. persistent headless engine;
3. fake-worker restart tests;
4. provider adapter boundary;
5. Gemini + DeepSeek behind that boundary;
6. transport abstraction and route health;
7. executable Weight of Time;
8. bounded Science Room test;
9. branch update/re-reference cycle;
10. GUI;
11. coding Workbench;
12. multiple project loops and cross-loop mobility.

This order makes the difficult persistent loop real before spending effort on presentation or broad autonomy.

# AI BRAIN BUDDY WORK — START HERE

## Purpose

This file is the handoff for any AI asked to work on Brain Buddy.

Brain Buddy is being developed as a persistent multi-AI collaboration system for One-Wave science and coding. Multiple AIs are EXPECTED to build competing implementations so their approaches can be tested and compared.

Do not assume the implementation written by the first AI is the final architecture.

## First rule: preserve working architecture

DO NOT edit `main` directly.

DO NOT overwrite another AI's working implementation branch.

DO NOT take an existing known-good branch and turn it into your experiment.

Create your own explicit child branch for substantial work.

Recommended naming:

`ai/<worker>/<goal>-<short-description>-YYYYMMDD`

Examples:

`ai/claude/goal01-core-contracts-20261002`
`ai/gemini/goal05-weight-of-time-20261002`
`ai/deepseek/goal06-dialogue-loop-20261002`
`ai/chatgpt/goal02-persistent-engine-20261002`

If you need several substantially different approaches, create separate branches for them rather than repeatedly rewriting one branch.

## Read before changing code

Read these architecture documents first:

1. `docs/BRAIN_BUDDY_PROJECT_GOALS_AND_BRANCH_GATES.md`
2. `docs/BRAIN_BUDDY_PLANNED_BUILD_STRATEGY.md`
3. `docs/BRAIN_BUDDY_SCIENCE_BASELINE_LOOP.md`
4. `docs/COUNCIL_CHAMBER_CHOICE_AND_INTERRUPT_MODEL.md`
5. `AI_ROUTING.md`
6. `GEMINI_OPTIONAL_EXECUTION_PROTOCOL.md`
7. `METADATA_AND_HANDOFF_CONTRACT.md`
8. `ai-route-manifest.json`
9. relevant skills under `skills/` and `chatgpt-plugin/`.

For One-Wave science work, Bridge-Comand is not the scientific authority. Reference the owning One-Wave Science repository and its canonical-start/reference rules first.

## Current implementation ancestry

Do not blindly rewrite from `main`.

Existing Brain Buddy implementation work has existed on branches including:
- `architecture/choice-rereference-reset-interrupts-20260930`;
- `recovery/brain-buddy-council-correct-home-20260930`;
- other recovery/known-good branches.

The current architecture specification work is on:
- `architecture/brain-buddy-science-baseline-loop-20261001`.

Before coding, identify the strongest runnable implementation/checkpoint for the goal you are attacking. Record the exact parent branch and commit in your branch notes.

## What we need built

The explicit build sequence and gates are in:
`docs/BRAIN_BUDDY_PROJECT_GOALS_AND_BRANCH_GATES.md`.

The high-level order is:

`inventory known-good -> contracts -> persistent engine -> provider adapters -> transport lattice -> executable Weight of Time -> back-and-forth best-answer loop -> One-Wave reference bundle -> bounded Science Room -> Baseline Zero re-reference -> App -> Coding Workbench -> project loops -> cross-project Council -> voluntary AI mobility -> nested Weight of Time`

Do not jump ahead by destroying a lower-level working layer.

## Competing implementations are welcome

Different AIs may solve the same goal differently.

That is intentional.

For the same goal:
1. each AI works on its own branch;
2. preserve the same required external contracts where possible;
3. document architectural choices;
4. run the required tests;
5. record failures as failures;
6. keep real execution receipts/results;
7. compare implementations on behavior, reliability, recoverability, simplicity and compatibility;
8. integrate useful pieces later on a separate integration branch.

Do NOT merge one AI's experiment into another AI's branch merely to compare them.

Do NOT select a winner because of provider identity. Compare observable behavior and evidence.

## Worker roles are dynamic

No provider permanently owns the role of main questioner/orchestrator.

Eventually any sufficiently capable authorized AI should be able to occupy roles such as:
- QUESTIONER / ORCHESTRATOR;
- RESEARCHER;
- SCIENCE WORKER;
- CRITIC / ADVERSARIAL REVIEWER;
- VALIDATOR;
- CODER;
- TESTER;
- REPO EDITOR operating under branch rules;
- OBSERVER in WATCH/LISTEN/THINK;
- SPECIALIST temporarily admitted from another loop.

The role must be represented in session state rather than hard-coded to ChatGPT, Claude, Gemini, DeepSeek or any other provider.

### Main-questioner requirement

A worker occupying QUESTIONER/ORCHESTRATOR must be able to:
- load the current Baseline Zero;
- construct/reference the relevant problem state;
- ask other workers;
- continue useful work while workers are pending;
- admit returned results as new VIEWs;
- challenge and re-reference answers;
- preserve Weight of Time;
- request validation;
- recognize unresolved contradictions;
- coordinate branch-safe proposed updates;
- establish/re-reference a new Baseline Zero only after the owning repo's acceptance rules are satisfied.

Switching the main questioner MUST NOT erase the session, Weight of Time, worker state, evidence, Baseline Zero lineage or pending work.

## Weight of Time must survive your implementation

Do not replace Weight of Time with:
- a fixed number of rounds;
- a simple timeout;
- majority vote;
- everyone-waits-for-everyone synchronization;
- one giant transcript.

Carry meaningful unresolved history: disagreements, contradictions, attempted tests/derivations, missing evidence, failed paths, gate state, material worker results and Baseline Zero lineage.

Workers return asynchronously. A late result becomes a new VIEW.

## One-Wave Science rules

Science work follows:

`BASELINE ZERO -> ONE-WAVE LENS/CANON -> LOGIC/REFERENCE RULES -> NODES/CHAPTERS -> READ JETSON PIPELINE METADATA -> EXTERNAL EVIDENCE AS NEEDED -> COUNCIL/WEIGHT OF TIME -> VALIDATE -> BRANCH UPDATE OF NODES + CHAPTERS + WRITABLE CLAIM/REFERENCE RECORDS -> ACCEPTED COMMIT -> NEW BASELINE ZERO -> RE-REFERENCE WORKERS`

CERN/LIGO/other numeric metadata and Wave-transformed Jetson pipeline outputs are read-only evidence to the Council. Do not hand-edit them as part of science discussion.

## Transport philosophy

Do not constrain the design to whatever bridge works today.

Brain Buddy should operate on capabilities and adapter contracts. Candidate transports include:
- GitHub;
- HTTP/HTTPS/WebSocket;
- local process/stdin/stdout;
- filesystem watchers/queues;
- SSH/systemd on Linux/Jetson;
- PowerShell/PowerShell Remoting or another authorized Windows route;
- MCP/plugins/apps;
- vendor APIs/SDKs/CLIs;
- containers;
- future remote workers/message buses.

If your implementation requires a missing program/bridge, DOCUMENT IT explicitly:
- capability required;
- proposed program/protocol;
- machine/OS;
- authentication requirement;
- install/configuration requirement;
- why existing routes do not satisfy it;
- fallback alternatives.

Do not silently remove a required capability because the bridge is unavailable today.


## Laptop storage rule — NO hard repo copies

Brain Buddy workers MUST NOT create persistent full repository clones, mirrors, duplicate checkout trees, profile copies, or background repo-copy loops on Mark's laptop.

The laptop is NOT a repository replication target.

Preferred access order for laptop work:
1. GitHub/API/reference access without cloning;
2. existing authorized remote working copy on Jetson/build machine when execution requires a checkout;
3. narrow file retrieval/materialization for only the files actually required;
4. only when unavoidable, a bounded temporary workspace with explicit size/lifetime and cleanup.

A temporary laptop workspace MUST NOT become a hidden persistent clone. Record why it is required, where it lives, its expected maximum size, and when/how it is removed.

Do not configure background watchers, services, login jobs, profile-copy jobs, synchronization loops, worktree farms, caches, or recovery mechanisms that repeatedly copy repositories onto the laptop.

Before any AI proposes a laptop-side clone/copy as a convenience, it must choose a non-copying reference/remote route if that can satisfy the task.

Intentional working checkouts on Jetson or another designated build machine are allowed when execution genuinely requires them, subject to that machine's storage and branch rules.

## Required branch work note

Every AI implementation branch should add/update a small branch-local work note containing:

- worker/provider;
- goal number;
- parent branch;
- parent commit;
- branch name;
- intended change;
- files expected to change;
- external programs/bridges required;
- tests to run;
- current status: PLANNED / ACTIVE / BLOCKED / PASS / FAILED;
- actual receipts/evidence;
- known regressions;
- next smallest step.

Suggested path:

`brain_buddy/work_notes/<worker>-<goal>-<date>.md`

## Definition of PASS

PASS means the goal's tests actually ran and the observed results satisfy its gate.

PASS does NOT mean:
- code was written;
- a workflow was queued;
- an AI said it should work;
- a mock succeeded when the gate requires a real provider;
- a request file exists;
- a process started without a matching result.

Keep failures visible. They are useful comparison data.

## Integration rule

Do not integrate competing versions directly into `main`.

When multiple approaches are ready:

`known-good parent + candidate branches -> separate comparison/integration branch -> tests -> integrated checkpoint`

Only a repeatedly tested integrated checkpoint can later be considered for deliberate main promotion.

Preserve the pre-integration known-good state.

## Instructions for a newly assigned AI

When Mark asks you to start Brain Buddy work:

1. Read this file and the three Brain Buddy architecture/goal documents.
2. Inspect current known-good implementation branches and exact commits.
3. State which explicit GOAL you are attacking.
4. Create YOUR OWN child branch.
5. Add your branch work note.
6. Preserve existing contracts/architecture unless your goal explicitly proposes a replacement.
7. Build.
8. Test.
9. Record real evidence.
10. Stop at the goal gate.
11. If PASS, checkpoint the working version before beginning another substantial goal.
12. If FAILED, keep the failed branch and return to the last known-good parent for the next attempt.

The objective is not for every AI to write the same code. The objective is to build a system where different approaches can be compared without losing working architecture, and where eventually any authorized AI can serve as the main questioner while the shared Brain Buddy state remains continuous.

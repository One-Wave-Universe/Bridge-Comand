# Brain Buddy Science + Repo Loops Runtime

Status: recovery runtime target

The immediate objective is a usable Brain Buddy with two persistent loops: SCIENCE and REPO WORK. Do not wait for the future two-state-machine Jetson brain.

## Shared persistent core

Both loops share:
- stable session_id and request_id
- current Baseline Zero
- inherited Weight of Time
- worker registry and route health
- pending/admitted VIEWs
- durable receipts
- branch/checkpoint lineage

A restart or device change reloads this state rather than starting a new conversation.

## SCIENCE loop

Authority order:
1. owning science repo and canonical start/reference rules
2. relevant governed nodes and chapters
3. read-only Jetson metadata/pipeline evidence when needed
4. external public evidence when needed
5. Council worker reasoning
6. validation back against the owning repo

Cycle:
REFERENCE -> DEFINE CLAIM/TEST -> ASK WORKERS IN PARALLEL -> KEEP WORKING WHILE RETURNS ARE PENDING -> ADMIT EACH REAL RETURN AS A VIEW -> WEIGH/CHALLENGE/RE-REFERENCE -> VALIDATE -> UPDATE WRITABLE NODE/CHAPTER/CLAIM RECORDS ON A BRANCH -> CHECKPOINT -> NEW BASELINE ZERO -> CONTINUE

Jetson metadata is evidence, not science authority, and normal Council work does not rewrite pipeline outputs.

## REPO WORK loop

Authority order:
1. owning repo instructions/canon
2. current branch and known-good checkpoint
3. exact task files
4. tests/build/runtime receipts

Cycle:
REFERENCE -> DEFINE CHANGE + ACCEPTANCE TEST -> CREATE/USE GOAL BRANCH -> ASK CODING/REVIEW WORKERS IN PARALLEL -> IMPLEMENT -> TEST -> ADMIT RESULTS -> REVIEW DIFF/REGRESSIONS -> CHECKPOINT KNOWN-GOOD -> NEW CHILD BRANCH FOR NEXT SUBSTANTIAL CHANGE

Never edit main directly. Failed experiments remain isolated from known-good.

## Cross-loop behavior

SCIENCE and REPO WORK run independently and may be active at the same time. Each has its own Weight of Time and current Baseline Zero lineage.

A loop may REQUEST-ENTRY or REQUEST-REVIEW from workers in the other loop. Admission begins WATCH/LISTEN/THINK before participation unless an explicit bounded task was requested.

Material findings can cross between loops only with provenance. Repo implementation does not make a science claim true; science discussion does not make an implementation tested.

## Worker behavior

Provider transports are adapters. Gemini, DeepSeek, ChatGPT, Claude, or later workers may use different routes.

Workers launch independently. No round barrier is required. While one worker is pending, available workers continue useful work. A late return is admitted as a new VIEW if its request_id and reference state are valid.

Provider failure is isolated. It does not stop the other loop or erase state.

## Minimum usable runtime gate

Brain Buddy is usable for daily Science + Repo work when all of these are demonstrated with real receipts:
- persistent session can start/resume
- SCIENCE loop can load its reference chain
- REPO WORK loop can load repo/branch/known-good state
- Gemini returns through a proven adapter
- at least one second independent worker returns through a proven adapter
- workers can be pending concurrently
- a return becomes a VIEW without stopping other work
- Weight of Time survives restart
- a science update can branch/checkpoint and establish a new Baseline Zero
- a repo change can branch/test/checkpoint
- device disconnect/reconnect does not lose loop state
- provider failure does not kill the loop

Future Jetson two-state-machine brain is a separate later capability. The current runtime may use the Jetson for bridges, workers, metadata pipelines, and machine-local evidence without depending on that future brain.


## Exploration -> attack selection -> simulation -> collaborative coding

The Science loop is not only an answer loop. Before committing to an attack, available AIs may explore competing directions together.

Exploration cycle:
PROPOSE TARGETS -> CHALLENGE PRIORITY -> IDENTIFY MISSING EVIDENCE -> DEFINE SIMULATOR/DERIVATION/EXPERIMENT NEEDED -> CHOOSE A BOUNDED ATTACK -> CREATE WORK PACKETS -> RUN IN PARALLEL -> COMPARE RESULTS -> CONTINUE OR PIVOT

Each proposed attack should state:
- exact claim/question
- why it is currently unresolved
- governing One-Wave references
- strongest known external constraint
- what would falsify or weaken it
- cheapest useful next test
- whether the next tool is algebra/derivation, numerical simulator, visualization, metadata query, literature search, hardware experiment, or code
- simulator inputs, outputs, invariants, acceptance criteria, and provenance requirements

Do not build a simulator merely because one can be built. Council first states what uncertainty the simulator resolves and what result would change the next decision.

### Collaborative coding

Coding is a Council activity, not a single-worker handoff.

For a selected software/simulator task:
1. establish a known-good parent checkpoint
2. create separate implementation branches/work packets when workers are trying materially different approaches
3. one or more workers may implement while others inspect references, derive equations, design tests, or review
4. workers publish branch/commit plus actual test receipts
5. reviewers compare observable behavior, scientific assumptions, tests, regressions, simplicity, and recoverability
6. integrate accepted pieces on a separate integration branch
7. rerun acceptance tests after integration
8. checkpoint only the tested integrated state

Workers must not overwrite one another's active branches. Competing code is preserved until Council has evidence for integration/rejection.

### Simulator registry

Maintain a project-visible registry of requested and existing simulators with:
- simulator_id
- scientific question
- owning repo/node/chapter
- status: PROPOSED / BUILDING / RUNNABLE / VALIDATED / REJECTED
- implementation branch/commit
- required datasets/metadata
- equations/assumptions
- test/validation receipts
- outputs/artifacts
- unresolved limitations

Science Council can request a simulator from Repo Work. Repo Work returns implementation/test evidence; Science Council interprets the result against the original scientific question. Passing software tests does not itself validate the scientific model.


## Build notes — differential weighting, nested Weight of Time, and live loop interaction

Status: design notes to preserve for implementation experiments. These are architecture targets, not claims that the runtime already implements them.

### Differential option ladder

Brain Buddy should not reduce competing options to isolated confidence scores. Explore a differential ladder centered on a real unresolved/HOLD state:

`A strongly favored <- A favored <- A leaning <- (0 / unresolved) -> B leaning -> B favored -> B strongly favored`

The ladder represents the current differential between competing options. Do not import CELL_V1 electrical threshold values into Brain Buddy merely because the topology is similar; Brain Buddy needs its own experimentally justified transition rules.

Agreement does not add weight. Multiple workers repeating the same claim, sharing the same source, or inheriting the same unsupported assumption are alignment, not independent confirmation. Track shared ancestry/provenance so duplicated support cannot create a house-of-cards effect.

Independent evidence, independent tests, survived challenges, contradictions, and falsification may change the differential. A decisive falsification must be able to collapse downstream dependent conclusions regardless of how many workers agreed with them.

### Weight of Time — nested asynchronous loops

Weight of Time is NOT a confidence score, consensus counter, or elapsed-time bonus.

It arises from loops within loops running asynchronously. While one loop is still cycling on a longer task, other loops continue doing useful cycles rather than blocking. By the time the loops reconverge, different loops may have accumulated different amounts and kinds of work/state transition.

`NESTED LOOPS -> UNEQUAL OPPORTUNITY TO CYCLE -> ACCUMULATED WORK/STATE -> RECONVERGENCE -> DIFFERENTIAL EVALUATION -> NEW SHARED STATE -> CONTINUE`

More wall-clock time alone adds no weight. More agreement adds no weight. More cycles alone do not prove correctness. The important state is what useful work, tests, contradictions, references, derivations, or discoveries occurred during those cycles.

A slow loop may return one decisive result that overturns many faster cycles. Fast loops may discover contradictions that change how a later slow result is interpreted.

A higher-level HOLD must not mean inactivity. It can preserve an unresolved choice while child loops continue working.

### Listen/evaluate/interject while loops are cycling

Workers need not wait for another loop's final return. An admitted loop/worker may observe available intermediate state from still-cycling loops, evaluate it, and selectively interject without forcing those loops to terminate.

Target behavior:

`CYCLE -> OBSERVE/LISTEN -> EVALUATE -> INTERJECT OR REMAIN SILENT -> RECEIVING LOOP ABSORBS INPUT -> CONTINUE CYCLING -> RECONVERGE`

An interjection is input, not evidence merely because another AI supplied it. Useful interjections include contradictions, missing references, invalid assumptions, independent evidence, duplicated-work detection, dependency changes, test results, or questions that materially change the attack. Mere agreement should normally remain silent.

The runtime needs an intervention threshold/rule so workers do not flood one another with low-value chatter.

### Think-before-speak <-> speak-before-thinking differential

Explore a second live differential controlling when a worker exports internal state:

`THINK / COMPRESS <- strong - moderate - slight - (0) - slight - moderate - strong -> SPEAK / EXPRESS`

THINK-FIRST: do more internal work before exporting a VIEW.
SPEAK-FIRST: expose an immature/reversible thought early so other loops can begin working on it while the originating loop continues thinking.

Neither direction is inherently superior and neither creates evidentiary weight.

Factors that should push toward THINK-FIRST include expensive/irreversible action, repo mutation, scientific claims, unresolved assumptions, high dependency depth, or consequences requiring validation.

Factors that should push toward SPEAK-FIRST include exploration, brainstorming, cheap reversible proposals, exposing a contradiction, requesting another loop's perspective, or starting useful parallel work early.

Speaking early creates a VIEW, not a commit or accepted truth. Thinking longer does not make a result true. Admission, provenance, reference checks, evidence, tests, and validation determine what may enter a new Baseline Zero.

### Evidence/dependency graph candidate

Do not make an opaque neural network the authority for these decisions. Explore an explicit inspectable graph/state model in which QUESTION/OPTION, VIEW, EVIDENCE, CHALLENGE/TEST, RESULT, and REFERENCE relationships can be traced.

AI agreement belongs in VIEW/alignment state rather than evidence weight. Track evidence ancestry and downstream dependencies. If a foundational assumption is falsified, dependent conclusions must be discoverable and marked for re-reference/re-evaluation instead of continuing to stand on inherited weight.

A neural model may later help retrieve, propose, cluster, or detect relationships, but should not silently replace the explicit provenance/differential state.

### Build questions to resolve experimentally

Before locking implementation, test:
- representation of pairwise/multi-option differential ladders;
- transition rules and whether seven bands are sufficient;
- how useful cycle/state changes are represented without turning cycle count into authority;
- what intermediate loop state is safe/useful to expose;
- intervention thresholds and anti-chatter controls;
- how THINK<->SPEAK state changes dynamically;
- provenance/shared-ancestry detection;
- dependency invalidation and re-reference propagation;
- reconvergence rules when slow decisive results meet many fast intermediate cycles;
- persistence/restart behavior for nested loops and their partial state.

Treat these as build/research questions. Branch competing implementations and compare behavior with receipts before promoting a mechanism into Brain Buddy canon.

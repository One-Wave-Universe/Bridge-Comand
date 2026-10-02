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

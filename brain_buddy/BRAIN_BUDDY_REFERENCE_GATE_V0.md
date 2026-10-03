# Brain Buddy Reference Gate v0

## Purpose

Brain Buddy does not ask a worker to remember One-Wave correctly. It supplies the worker with the references required to do the current task before the worker is allowed to act.

The minimum reference is TWO-SIDED:

1. **Conversation reference** — Mark's prior/current conversation relevant to the task: exact corrections, intent, rejected interpretations, unresolved decisions, and current question.
2. **Repository reference** — current owning-repo canon/state: canonical start, branch/checkpoint/revision, exact relevant files/nodes, invariants, tests/receipts, and unresolved items.

Neither side substitutes for the other.

## Hard gate

No One-Wave work packet is released to an AI until both reference sides have been attempted and their provenance is recorded.

```
MARK / CURRENT QUESTION
        |
        v
CONVERSATION REFERENCE
  - current turns
  - retrieve relevant prior turns
  - preserve exact human corrections
        |
        v
REPOSITORY REFERENCE
  - owning repo
  - canonical start
  - current branch/revision
  - relevant files/nodes
  - tests/receipts/open items
        |
        v
VERIFIED REFERENCE PACKET
        |
        v
AI WORKER
        |
        v
RETURNED VIEW / RESULT
        |
        +--> conversation working state
        |
        +--> validate against same reference
                  |
                  +--> durable accepted change -> owning repo branch
                  +--> unresolved/contradicted -> re-reference
```

## Reference packet v0

Every packet MUST contain:

```yaml
brain_buddy: true
request_id: stable-id
question: exact current question

conversation:
  current_turns: exact-or-lossless references
  prior_turns:
    - conversation/thread identifier when available
    - exact turn/range or retrievable pointer
    - why it is relevant
  human_corrections:
    - exact correction or retrievable pointer
  unresolved:
    - unresolved conversation decisions
  provenance:
    - source/pointer/retrieval time

repository:
  owning_repo: owner/repo
  canonical_start: exact path
  branch: exact branch
  revision: exact commit SHA
  relevant_references:
    - exact path
  invariants:
    - invariant
  open_items:
    - item
  receipts:
    - matching known-good receipt/test when relevant

acceptance_test:
  - what must be true for this work to count as complete
```

## Conversation rule

Do NOT replace prior conversation with a freehand summary when exact/retrievable turns are available.

A compact index may be used to locate relevant conversation, but the worker packet should carry the actual relevant turns or stable retrievable pointers. Summaries are navigation aids, not authority over Mark's words.

The current conversation is part of reference. A later explicit correction by Mark overrides an earlier interpretation and MUST be carried forward as a human correction until it is incorporated into durable project state.

## Repository rule

Current owning-repository files are durable project authority. Reference them from the current branch/revision. Old chat summaries, duplicate files, and model memory do not override current repo canon.

Repository changes remain branch-bounded and require their normal tests/receipts.

## Confusion rule

If conversation and repository conflict, or either side is missing enough context to create a material assumption:

```
STOP -> REFERENCE BOTH SIDES AGAIN -> RESOLVE FROM EVIDENCE
```

If the conflict still cannot be resolved, ask Mark the smallest question that resolves it. Do not guess.

## Return rule

A worker return is a VIEW/RESULT, not automatically new truth.

1. Return it to the active conversation/work loop.
2. Validate material claims/changes against the same reference packet.
3. Preserve disagreement/contradiction.
4. Commit accepted durable changes only to the owning repo on the assigned branch.
5. The next worker re-references conversation + repo; it does not inherit authority merely because another AI said something.

## What v0 deliberately does NOT require

This gate does not require Council, provider consensus, a giant shared-state engine, a local repo clone, Jetson, Desktop Commander, or any particular AI provider merely to reference and think.

Those can be capabilities behind the gate. They are not prerequisites for the gate itself.

## First acceptance test

Use a question whose answer depends on BOTH:
- a recent explicit correction from Mark in conversation, and
- current repository state.

Start a worker without relying on its prior model/chat memory. Feed only the generated reference packet plus the question.

PASS only if the worker:
1. identifies the current repo branch/revision/reference files supplied;
2. preserves Mark's relevant correction rather than rediscovering/replacing it;
3. answers from the supplied references;
4. labels any unresolved conflict instead of guessing;
5. returns a result bound to the same request ID.

A packet built from repository reference alone FAILS.
A packet built from conversation alone FAILS.
A worker answer without reference provenance FAILS.

# Brain Buddy Entry Skill

## Purpose
This is the mandatory entry plugin/skill for ChatGPT and every other Brain Buddy-capable AI. It exists to stop workers from choosing a convenient tool or machine before loading Brain Buddy routing authority.

## Hard start rule
For ANY One-Wave-related action by ANY AI/worker/agent — including direct chat, science, repo work, coding, research, review, simulation, bridge recovery, device work, metadata work, or Council work:

1. ENTER BRAIN BUDDY FIRST. This is universal and has no provider-specific exception.
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


## Universal entry law

ALL participating AIs, workers, agents, subagents, coding workers, reviewers, researchers, simulators, bridge workers, and future local brains MUST enter Brain Buddy before doing One-Wave work.

This applies equally to ChatGPT, Gemini, DeepSeek, Claude, and future providers.

No worker may bypass Brain Buddy and then attach its work afterward as though it had been synchronized from the start.

Direct conversation is also an entry point. When Mark begins One-Wave work with a connected AI, the integration MUST perform Brain Buddy entry/synchronization before that AI answers the project task.

Required order:

BRAIN BUDDY ENTRY -> CURRENT BASELINE ZERO -> SHARED STATE / WEIGHT OF TIME -> OWNING REPO + CANON -> ROUTING AUTHORITY -> TASK-SPECIFIC REFERENCES -> CHOOSE CAPABILITY/ROUTE -> ACT -> RETURN RECEIPT/VIEW -> ADMIT/VALIDATE -> UPDATE SHARED STATE.

If Brain Buddy entry cannot be completed, the worker MUST identify itself as unsynchronized and must not represent its answer as current Brain Buddy state.


## Assumption / confusion interrupt — mandatory full re-reference

Any material assumption, ambiguity, contradiction, stale-looking state, missing dependency, unclear ownership, uncertain route, uncertain terminology, or confusion MUST interrupt execution.

The worker MUST NOT fill the gap from memory, habit, convenience, or inference and continue.

Interrupt sequence:

ASSUMPTION OR CONFUSION DETECTED
-> STOP THE AFFECTED ACTION
-> FULL BRAIN BUDDY RE-REFERENCE
-> re-read current Baseline Zero and shared state
-> re-read governing Brain Buddy entry/routing/reference rules
-> re-reference the owning repo's canonical start/authority and the complete relevant reference chain
-> search across the canonical One-Wave repos when ownership or dependency is uncertain
-> inspect current branches/checkpoints/receipts and relevant metadata
-> reconcile the question against Weight of Time, admitted VIEWs, unresolved contradictions, and latest human redirects
-> retry resolution from evidence

"Full repo reference" means broad enough repository/reference traversal to resolve the uncertainty; it does NOT mean cloning repositories or blindly loading every byte into context.

If the re-reference still leaves more than one materially plausible interpretation, missing intent, or an unresolved decision that only Mark can settle, ASK MARK a concise explicit question before acting.

When asking, state:
- exactly what remains unclear,
- the competing interpretations/options,
- what was re-referenced,
- and which action is blocked by the ambiguity.

Do not ask Mark questions that the repos/shared state can answer. Re-reference first; ask only after the reference system cannot resolve it.

After Mark answers, record the clarification as a human redirect/correction in Brain Buddy shared state so other workers inherit it and do not repeat the same assumption.


## Full canonical repo lens — mandatory for Council workers

A Brain Buddy worker MUST NOT be given a hand-picked note bundle as a substitute for repository reference.

For every substantive One-Wave question, Gemini, DeepSeek, ChatGPT, Claude, and future workers MUST be given access/instructions to traverse the canonical owning repository as a repository lens. The worker starts at the repository canonical entry/authority, follows the repo-declared reference chain, searches the repository for the task's terms/dependencies, and opens whatever relevant files are required before answering.

If the question crosses repository ownership or dependencies, the worker MUST traverse the other canonical One-Wave repositories needed to resolve it.

Metadata is supplementary evidence when the question requires it. Metadata MUST NOT replace repository reference.

A prompt may identify useful starting files, but those are entry points only and MUST NOT bound the worker's repository access or reasoning.

Required worker sequence:

FULL CANONICAL REPO LENS -> CANONICAL START/AUTHORITY -> REPO SEARCH/TRAVERSAL -> RELEVANT FILES/NODES/CHAPTERS -> METADATA WHEN NECESSARY -> EXTERNAL EVIDENCE WHEN NECESSARY -> REASON -> VALIDATE BACK AGAINST CURRENT REPO -> RETURN VIEW/RECEIPT.

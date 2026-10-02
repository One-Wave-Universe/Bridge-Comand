# Brain Buddy Science Baseline Loop

## Authority

For One-Wave science work, the owning One-Wave Science repository is the scientific authority. Bridge-Comand transports and coordinates work; it does not replace Science canon.

## Required science loop

Every science task follows this outer loop:

`BASELINE ZERO -> ONE-WAVE LENS/CANON -> LOGIC/REFERENCE RULES -> RELEVANT NODES/CHAPTERS -> READ JETSON PIPELINE METADATA -> EXTERNAL SOURCES WHEN REQUIRED -> COUNCIL WORK/DEBATE -> WEIGHT OF TIME -> VALIDATE -> UPDATE NODES + CHAPTERS + CLAIM/REFERENCE RECORDS -> COMMIT -> NEW BASELINE ZERO -> RE-REFERENCE ALL WORKERS`

### Reference before reasoning

Before a worker reasons about a One-Wave claim it must receive or retrieve:
- current Baseline Zero commit/ref;
- One-Wave lens and canonical-start/reference rules;
- exact relevant nodes and chapters;
- relevant Jetson pipeline metadata and its provenance/transform/version references, plus assumptions, gates and unresolved tests;
- external/public evidence when the claim requires real-world comparison or verification.

Internet/public sources are evidence inputs, not automatic One-Wave canon. Preserve provenance and separate established external results from One-Wave interpretation and unverified hypotheses.\n\n### Jetson pipeline metadata is read-only evidence\n\nCERN, LIGO and other source-data pipelines on the Jetson produce numeric metadata and Wave-transformed data. Brain Buddy MUST NOT rewrite, hand-edit, reinterpret in place, or regenerate those pipeline outputs as part of a science discussion/update. The Council may query/read them and record the exact dataset, source, pipeline/transform, version/hash and retrieval reference it used. Changes to a pipeline or its generated data are a separate pipeline/code task with their own validation and provenance.

### Weight of Time Council

Workers do not wait for synchronized rounds. Available workers continue useful work while other workers are unresolved. A returned result becomes a new VIEW and may be challenged, expanded, re-referenced or sent back through another worker.

The Council continues while useful unresolved weight remains: material disagreement, missing evidence, unresolved contradiction, failed validation, or a materially better supported formulation still developing. Do not reduce this to a fixed round count or arbitrary answer timer.

### Settlement and validation

A candidate result may update Science only after:
1. re-reference against current Baseline Zero;
2. check against One-Wave logic/reference rules;
3. verify cited Jetson pipeline metadata and external evidence without modifying pipeline outputs;
4. preserve established / derived / simulated / hypothesis / unverified distinctions;
5. identify affected nodes, chapters and metadata;
6. check that the proposed edits agree with each other.

### Atomic science update

An accepted scientific change updates the complete affected reference set together:
- node files;
- affected book/chapter text;
- writable claim/gate/provenance/reference records that point to the exact read-only pipeline metadata used;
- indexes/cross-references required by Science canon.

Do not update a chapter while leaving its governing node stale, or update a node while knowingly leaving an affected chapter inconsistent.

### New Baseline Zero

After validation, commit the coherent Science update. The accepted commit becomes the next Baseline Zero for that task lineage.

Before any Council worker continues downstream science reasoning, provide or require the new Baseline Zero and re-reference the affected canon. No worker's stale transcript or private context outranks the committed baseline.

### Git safety

Council reasoning may propose edits, but experimental work stays on branches until validated. Canonical updates follow the owning repository's merge/authority rules. Receipts prove worker returns; they do not make a scientific claim true.


## Branch-first development law

Until a solid, repeatedly tested Brain Buddy version is deliberately established as the canonical main baseline, all Brain Buddy changes remain branch work.

- Do not develop directly on `main`.
- Each substantial architecture change, AI/provider adapter, loop evolution, Science Room change, Workbench change, pipeline/code change, or recovery experiment gets an explicit branch.
- A working evolution is checkpointed before the next substantial evolution branches from it.
- Failed experiments remain isolated and must not destabilize a known-good branch.
- Science edits produced by Brain Buddy are also proposed and validated on branches under the owning Science repository's authority before canonical merge.
- Establishing a new `main` baseline is a deliberate promotion after repeatable execution, validation, restart/recovery testing, and preservation of the last known-good state.
- After promotion, that canonical commit becomes the development Baseline Zero; subsequent evolution branches from it rather than editing it in place.


## Weight of Time is inherited state

Weight of Time is not a temporary discussion mode and MUST NOT be discarded by later Brain Buddy versions, UI rewrites, provider changes, restarts, commits, or Baseline Zero promotion. Future implementations may expand it but must preserve its core behavior.

For each unresolved problem, carry forward enough state to reconstruct why the current position exists:
- competing views and material disagreements;
- attempted derivations/tests and their outcomes;
- contradictions and unresolved questions;
- evidence acquired and evidence still missing;
- failed or rejected paths and the reason they failed;
- current claim/gate state and provenance;
- worker results that materially changed the problem;
- references to the Baseline Zero states under which those results were produced.

Elapsed wall-clock time alone is not Weight of Time. Weight grows from unresolved work and its accumulated consequence/history.

### Expansion rule

A later result is a new VIEW over the accumulated state, not a replacement for earlier unresolved state. Workers may re-open a settled-looking answer when new evidence creates a material contradiction or better-supported path.

When a new Baseline Zero is established, compress the resolved history into the canonical nodes/chapters/claim records while retaining references to unresolved weight. Do not erase unresolved contradictions merely because a commit was made.

Every worker entering or re-entering the Council receives:
1. the current Baseline Zero;
2. the current problem state;
3. the material inherited Weight of Time;
4. the exact references/evidence needed to continue.

The purpose is continuity of reasoning across workers, sessions and generations of Brain Buddy without forcing every worker to replay the entire raw transcript.


## Voluntary cross-loop entry

A worker may recognize that another active project/problem loop is relevant and request permission to enter it. Cross-loop participation is requested, not assumed.

A `REQUEST-ENTRY` should identify:
- requesting worker and its current loop;
- target loop;
- why entry is useful now;
- the evidence, contradiction, dependency or capability motivating the request;
- the requesting worker's relevant Baseline Zero/reference state.

The target loop owns admission. It may:
- `ADMIT` now;
- `DEFER` until an appropriate loop boundary;
- `DECLINE` with a reason.

Admission does not give the entering worker authority to rewrite the target project's canon. On admission, the worker must re-reference the target loop's current Baseline Zero, governing lens/rules, relevant state and inherited Weight of Time before contributing.

An entering worker's prior context is evidence/context, not authority over the target loop. Results produced inside the target loop follow that loop's validation and branch rules.

This mechanism should later support project loops voluntarily convening, borrowing workers, requesting specialist review, and returning useful results to their owning loops without collapsing all projects into one shared context.

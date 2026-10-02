# Bridge Command — Canonical Recovery and Operations

This repository is the single authority for One-Wave bridge, relay, remote-execution, metadata, and AI-to-AI transport work.

## Operating law

REFERENCE GIT -> ASK/PIVOT -> REFERENCE METADATA/CENTER-FLIP -> VALIDATE/PIVOT -> UPDATE REFERENCE/CENTER-FLIP -> REFERENCE.

Every flip returns through the reference. Do not declare a bridge healthy because files, services, queues, or workflows exist. A route is healthy only after an end-to-end receipt from the requested endpoint.

## One authority, live connections, no copies

- Bridge-Comand owns bridge and relay contracts.
- One-Wave-Science owns science claims, models, evidence rules, and scientific source interpretation.
- Builds owns runnable build artifacts.
- A device service must point to the canonical existing checkout or an explicitly named runtime cache. A runtime cache is never a second authority.
- Do not create another bridge repository, paste bridge doctrine into Science, or treat a generated worktree as canon.
- Connect agents to the owning repository and record the repository URL, branch, commit SHA, and reference files in every receipt.

## Reference -> Build -> Check — mandatory build law

For any build, repair, recovery, bridge, worker, Brain Buddy, or runtime task, **REFERENCE does not mean merely reading design documentation**. REFERENCE means reconstructing the authoritative real state that the next change must inherit.

Before writing or changing code, recover and record, in this order:

1. **Canonical authority** — this file plus the owning repository's canonical start/reference rules.
2. **Last successful observable result** relevant to the requested capability. Search receipts, responses, sessions, outputs, completed runs, workflow/job logs, and returned endpoint results. Prefer the last proven success over the latest commit.
3. **Receipt/result provenance** — request ID, timestamp, provider/worker, actual returned content/result, and acceptance condition that made it a success.
4. **Exact implementation that produced that result** — executable/entry point, caller, adapter/bridge/relay, trigger/listener/workflow/service, and state/session files.
5. **Exact source state** — repository, branch, commit SHA, and relevant file SHAs/paths.
6. **Exact execution path** — where execution starts, every transport boundary it crosses, where credentials/auth are supplied, and where the return comes back.
7. **Current divergence** — compare the known-good state to the current state and identify the first changed or broken boundary.

For recovery work, use this chain explicitly:

`LAST SUCCESSFUL RESPONSE -> RECEIPT/SESSION -> CODE THAT PRODUCED IT -> COMMIT SHA -> EXECUTION/TRIGGER PATH -> AUTH/TRANSPORT -> RE-RUN SAME PACKET -> MATCHING RETURN RECEIPT`

**Do not use "latest commit" as a substitute for known-good. Do not design a replacement from documentation while a prior working implementation can be recovered. Do not BUILD until the reference chain reaches a real executable entry point and its return path.**

### BUILD

Build from the recovered known-good source state on a new recovery/goal branch.

- Preserve the working entry point and return path unless the bounded task specifically requires changing them.
- Change the smallest boundary needed.
- Do not collapse providers, transports, authentication methods, worker identities, state, provenance, receipts, or evidence sources into a common mechanism merely because they serve a common Brain Buddy contract.
- Provider adapters remain provider-specific. A shared envelope is not permission to replace native transports.
- Never replace a working logged-in/session route with an API route, or an API route with a session route, without explicit evidence and an explicit task requiring that change.
- A build is incomplete if no reachable trigger/entry point can execute it.

### CHECK

CHECK means execute the real entry point through the intended path and observe the requested endpoint return.

- Source inspection, file existence, syntax success, queue creation, workflow launch, service-active state, listener presence, or dispatch success are **not** endpoint PASS.
- Require the same request ID across request and return when the contract supports it.
- Record actual transport, provider/worker identity, reference state, result, and failure boundary.
- If the endpoint does not return, mark `FAILED` or `BLOCKED`; do not describe the build as working.
- After CHECK, return to REFERENCE. The observed result becomes part of the next authoritative state.
- If CHECK fails, reference the last known-good chain again before the next BUILD. Do not stack speculative fixes.

The mandatory loop is:

`REFERENCE REAL STATE -> BUILD ONE BOUNDED CHANGE -> CHECK REAL ENDPOINT -> REFERENCE OBSERVED STATE -> ...`

For Brain Buddy specifically, the persistent back-and-forth architecture coordinates independent workers; the reference is the authoritative state each loop crosses, not a replacement for the architecture. Council is a set of participating workers/views, not the Brain Buddy architecture itself.

## Brain Buddy application build contract — internal dialogue + nested parallel loops

When the requested product is Brain Buddy, the build target is a **working persistent application**, not a provider wrapper, sequential council script, prompt template, queue writer, or collection of disconnected bridges.

### Required runtime shape

The greater persistent loop is:

`REFERENCE -> BUILD/WORK -> CHECK/EVALUATE -> REFERENCE -> ...`

Inside that greater loop, multiple child loops run independently and concurrently:

`REFERENCE -> VIEW/QUESTION -> WORK/BUILD/DERIVE/SEARCH/TEST -> CHECK -> INTERJECT OR HOLD -> REFERENCE -> CONTINUE`

The greater loop must remain alive while child loops are pending. It must not impose a round barrier where every worker has to finish before useful work continues.

### Internal dialogue is mandatory

Brain Buddy must maintain an ongoing internal dialogue from admitted state, not merely send one prompt to several providers and concatenate their answers.

The dialogue must support both live tendencies:

`THINK/COMPRESS -> SPEAK/EXPRESS -> RE-EVALUATE`
and
`SPEAK/EXPRESS -> LISTEN -> THINK/COMPRESS -> RE-EVALUATE`

Neither tendency permanently controls. An early thought is a reversible VIEW, not truth. Longer thinking is not evidence by itself.

Each admitted participant/loop may:
- observe available current state and intermediate VIEWs;
- ask a question;
- challenge an assumption or reference;
- expose a contradiction;
- request evidence, a derivation, a test, a build, or another VIEW;
- interject while another child loop is still working when the intervention is material;
- remain silent when it has no useful differential contribution;
- revise its own prior VIEW;
- HOLD an unresolved choice without stopping child work.

Mere agreement should not generate chatter or evidentiary weight.

### Parallel-loop requirements

At minimum, the runtime must be capable of maintaining concurrently:
- a reference/re-reference loop;
- at least two independent worker/reasoning loops;
- a build/work loop when the task requires action;
- a check/validation loop;
- persistence/receipt handling that does not block useful reasoning.

Provider workers are optional participants in these loops, not the architecture itself. Gemini, DeepSeek, ChatGPT/OpenAI, Claude, local workers, metadata readers, repo workers, and later workers retain their own native transport, authentication, state, capabilities, failures, and provenance.

Do not collapse independent workers into one provider call. Do not fake parallelism by executing a fixed sequential list and labeling the combined output "parallel."

### Views up / actions down

Brain Buddy must distinguish observation/reasoning from mutation/action.

Views move upward into shared evaluation state. Actions move downward only after the current state permits the bounded action and its acceptance check is known. Preserve Field/Void or equivalent opposing/complementary views as separate inspectable state rather than averaging them into a hidden score.

An action result returns upward as a new observed VIEW/CHECK result and must cross REFERENCE again before further consequential action.

### Weight of Time

Weight of Time is persistent unresolved/accumulated working state created by nested asynchronous loops. It is **not** elapsed wall time, provider agreement count, confidence score, or number of cycles.

Persist:
- unresolved questions and contradictions;
- pending child loops and request IDs;
- admitted VIEWs and their provenance;
- useful tests/builds/evidence produced while other loops were pending;
- dependencies between assumptions, evidence, results, and conclusions;
- current HOLD states;
- interventions and why they were admitted;
- branch/checkpoint lineage;
- last known-good executable state.

When loops reconverge, evaluate what changed. A slow decisive result may overturn many fast intermediate cycles.

### Reconvergence and reference crossing

Every child-loop return enters as a VIEW with provenance. The greater loop evaluates it against the current reference and dependency state.

Reconvergence must be able to:
- preserve disagreement;
- detect duplicated/shared evidence ancestry;
- invalidate downstream conclusions when a dependency is falsified;
- create or maintain HOLD;
- choose the next bounded question/build/test;
- establish a new Baseline Zero only after the required validation/check;
- continue without erasing minority/contradictory VIEWs.

Every meaningful flip crosses the reference/center again.

### Persistence and restart

The application must resume the same live dialogue after restart or device change. Persist enough state that restart does not turn Brain Buddy into a new conversation.

A resumed session must restore:
- session ID and Baseline Zero/reference state;
- Weight of Time;
- child-loop state: pending/running/returned/admitted/held;
- VIEWs, questions, contradictions, and provenance;
- action/build/check state;
- receipts and request IDs;
- worker route health;
- branch/checkpoint lineage.

On restart, reconcile uncertain executions before retrying them. Never blindly duplicate an action whose completion is unknown.

### Usable application surface

Provide one clear runnable entry point for a human to:
- start a Brain Buddy session with a question/task;
- resume an existing session;
- inspect the current internal dialogue/state;
- add or redirect a question;
- see which loops/workers are running, pending, held, failed, or returned;
- see admitted VIEWs and contradictions;
- see proposed/authorized actions and their checks;
- stop and resume without losing state.

The first version may be CLI/TUI/web/app, but it must be directly runnable and must drive the real runtime. A source file with no reachable trigger is not an application.

### Build order

Do not attempt the whole target as an unverified rewrite.

1. REFERENCE the last proven back-and-forth implementation using the mandatory known-good chain above.
2. Re-run the same known-good packet unchanged and require its matching returned receipt.
3. Branch from that exact known-good source state.
4. Preserve its working transports/auth/return paths.
5. Add durable session/resume if absent; CHECK restart/resume.
6. Add two truly independent concurrent child loops; CHECK that one can continue while the other is pending.
7. Add admitted VIEW state and internal dialogue; CHECK challenge/revision/interjection behavior.
8. Add HOLD + Weight-of-Time persistence; CHECK across restart.
9. Add build/action authorization and real CHECK return; CHECK that dispatch alone cannot PASS.
10. Add reconvergence/dependency/provenance handling; CHECK contradiction and falsification cases.
11. Add/finish the human application surface.
12. Run the complete acceptance suite repeatedly before promotion.

After every numbered build step: `CHECK REAL BEHAVIOR -> REFERENCE OBSERVED STATE`. Do not stack the next feature on a failed step.

### Minimum acceptance suite

Brain Buddy is not a working app until receipts/tests demonstrate all of the following:
- launch a new persistent session;
- resume the same session after process restart;
- recover the named reference and known-good lineage;
- run at least two child loops concurrently;
- prove useful work continues while one child loop is pending;
- admit a returned worker result as a VIEW without treating it as truth;
- produce internal dialogue in which a VIEW is challenged, revised, or materially interjected upon;
- preserve a genuine disagreement/HOLD without forcing consensus;
- preserve Weight of Time across restart;
- keep provider identity, transport, auth mode, state, and provenance distinct;
- execute one bounded real action/build and observe its endpoint CHECK;
- refuse to mark dispatch/queue/workflow-start as endpoint PASS;
- survive one worker/provider failure while other loops continue;
- admit a late valid return without corrupting current state;
- prevent duplicate execution when completion is uncertain;
- trace a conclusion to its VIEW/evidence/reference dependencies;
- invalidate/re-reference a dependent conclusion after a foundational test fails;
- stop and resume without losing the internal dialogue;
- expose the above behavior through the runnable human entry point.

A test harness may use deterministic fake workers to prove concurrency, restart, HOLD, dialogue, and dependency behavior, but **provider/transport acceptance requires real endpoint receipts from the intended providers**. Fake-worker tests can prove the engine; they cannot prove Gemini, DeepSeek, GitHub, Jetson, or another external route.

### Definition of failure

Reject the implementation as incomplete if it is:
- a sequential provider loop;
- a one-shot council query;
- a prompt that asks providers to simulate internal dialogue;
- a queue/dispatch system without returned results;
- a state file with no runnable engine;
- an engine with no reachable human entry point;
- a provider abstraction that erases transport/auth/provenance differences;
- an app that loses dialogue/Weight of Time on restart;
- an app that waits for all workers before doing anything useful;
- an app that calls agreement evidence or calls dispatch success execution success.

## Directions for every AI client

Codex, ChatGPT, Gemini, Claude, DeepSeek, Perplexity, local Qwen/OpenClaw, phone relays, and future clients use the same loop:

1. Read this file and the owning repository's canonical start file.
2. Record repository, branch, commit SHA, exact question, and named reference paths.
3. Ask the bounded question through the smallest live lane.
4. When a conclusion depends on measured numbers, declare `numeric_evidence_required: true` and attach bounded science metadata requests. Do not invent, remember, or silently substitute numbers.
5. Keep provider material separate from One-Wave interpretations.
6. Validate the response against the named repository references and metadata provenance.
7. Return a receipt containing route, request ID, references actually read, metadata actually read, exit/result state, and unresolved gaps.
8. Update only the owning repository when warranted, then reference the new commit again.

Required status words are: `ESTABLISHED`, `IMPLEMENTED`, `TESTED`, `UNVERIFIED`, `HYPOTHESIS`, `ASSUMPTION`, `FAILED`, and `BLOCKED`.

## Current lanes

### Jetson / Hive Pipe MCP

Canonical remote contract uses Hive Pipe MCP `terminal_run`.
Required command fields: `argv`, `timeout`, `intention`, `consequence`; `cwd` when needed.
Never put credentials in tracked files or logs.

Expected Jetson credential locations:

- `~/.config/hive-pipe/tokens/codex.token`
- legacy migration source: `~/.config/hive-pipe/gateway.token`
- optional client environment: `~/.config/hive-pipe/remote.env`

GitHub Actions expects repository secrets `JETSON_GATEWAY_URL` and `JETSON_GATEWAY_TOKEN`. Restore them from the live Jetson configuration. Never manufacture a replacement token merely to make a test pass. Never commit their values.

### Desktop Commander

Registered machines may exist while their transports are offline. Treat registration/auth-token validity, process state, service state, and transport-online state separately.

Persistent unit on both Linux devices:

`~/.config/systemd/user/desktop-commander-remote.service`

Required service properties:

- pinned agent version;
- `Restart=always`;
- enabled for `default.target`;
- user linger enabled so the service survives logout and starts at boot;
- saved registration under the user's home directory;
- no copied One-Wave repository.

Recovery order:

1. Query device state.
2. If online, run `hostname` and `id -un` and retain the receipt.
3. Inspect `systemctl --user show desktop-commander-remote.service -p ActiveState -p SubState -p UnitFileState -p MainPID -p ExecMainStatus`.
4. If offline, use an independent live lane to restart that service once.
5. Query device state again.
6. Run the harmless identity probe again.
7. Only then mark Desktop Commander `VERIFIED`.

Current handover state on 2026-09-29:

- `scales-Latitude-E7450` and `localhost.localdomain` have valid saved registrations.
- pinned version `0.2.51` user services were installed, enabled, active, and both accounts had `Linger=yes` before handover.
- after the old manual processes were terminated, both registered devices reported offline and did not reconnect within the observation window.
- therefore persistent Desktop Commander transport is `PARTIAL`, not verified. The first failing boundary is service-process-to-remote-transport reconnection. Restart the service from an independent lane and require a new online identity receipt.

### GitHub pull bridge

Primary and backup transport branches remain `chatgpt-terminal` and `chatgpt-terminal-backup` in One-Wave-Science until migration is explicitly completed. Write the same request ID and content to both and require a matching result ID. A stale result is not a response.

### GitHub Actions -> Jetson metadata

Active workflow: `.github/workflows/jetson-science-metadata.yml`.
Request directory: `.metadata-dispatch/`.

A live query must use a bounded HTTPS metadata/API endpoint. The Jetson performs the external query; GitHub is the dispatch/reference layer.

Current verified state:

- GitHub push dispatch works.
- run `36567405790` failed before Jetson contact because `JETSON_GATEWAY_URL` and `JETSON_GATEWAY_TOKEN` were absent.
- GitHub -> Jetson metadata transport remains `BLOCKED`, not end-to-end verified.

### Gemini repository lens

Gemini must use One-Wave-Science as a lens, not replace it:

`REFERENCE GIT -> ASK -> GEMINI RESPONSE -> VALIDATE AGAINST REFERENCE/METADATA -> UPDATE OWNING REPO IF WARRANTED -> REFERENCE`.

The GitHub-native request schema accepts named repository references and optional bounded science metadata:

```json
{
  "schema": "one-wave-github-gemini/v2",
  "id": "unique-request-id",
  "question": "One bounded question",
  "references": [
    {
      "repo": "One-Wave-Universe/One-Wave-Science",
      "ref": "main",
      "path": "exact/relevant/file.md"
    }
  ],
  "numeric_evidence_required": true,
  "metadata_requests": [
    {
      "provider": "GWOSC",
      "url": "https://gwosc.org/api/v2/event-versions/",
      "purpose": "Identify the exact catalog/event metadata needed by the question",
      "max_bytes": 250000
    }
  ]
}
```

The workflow automatically reads `One-Wave-Science/AI_CANONICAL_START_HERE.md` first, records every reference and metadata source actually read, hashes retrieved metadata, and tells Gemini to label evidence state. Metadata is consulted only when the request declares that measured numbers are required.

Current verified state:

- run `36566722396` reached the Gemini job but failed because `GEMINI_API_KEY` was absent.
- a queued request or workflow start is not a Gemini response.
- the Jetson CLI/OAuth lane is separate and must return its own matching receipt.

## Science metadata rules

Before external data:

1. reference One-Wave-Science canon and the exact test;
2. query metadata before bulk data;
3. inspect size before data;
4. use the smallest useful sample;
5. preserve provider, experiment/detector, record/event/catalog/version IDs, URL/API endpoint, release/version, retrieval time, units/calibration/quality fields, byte count, and content hash;
6. keep raw provider material separate from One-Wave-derived transformations;
7. treat retrieval as input evidence, not automatic scientific support;
8. never tune a frozen prediction after exposure to held-out evidence.

## Failure discipline

Change one thing -> test -> compare to goal -> check drift.
After three repeats of the same failure, change route or diagnostic angle.
Prefer receipts over explanations.
Do not create duplicate bridge doctrine in other repositories; point back here.

## Definition of done

A bridge is `VERIFIED` only when the requested endpoint completes and its return is read back through the intended path. File presence, service configuration, registration validity, queue creation, and workflow launch are intermediate states only.

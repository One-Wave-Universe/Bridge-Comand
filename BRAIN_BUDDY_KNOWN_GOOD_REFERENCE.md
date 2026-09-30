# Brain Buddy — Known-Good Reference

## Locked recovery baseline

- Repository: `One-Wave-Universe/Bridge-Comand`
- Proven Gemini receipt commit: `a17e84f8e5c57ae5d852586581ed66ffda128f37`
- Commit meaning: `Wire phone hub direct Gemini request and verified receipt`
- Recovery branch: `recovery/brain-buddy-known-good-20260930`

This branch exists to preserve and reproduce the last repository-proven Brain Buddy transport state. It is a REFERENCE BASELINE, not a development branch.

## NO-CHANGE / ALL-STOP LAW

**If any worker, AI, script, automation, repair process, or human is about to alter this known-good reference baseline: ALL STOP.**

Do not:
- edit the known-good implementation in place;
- rewrite or force-move this recovery baseline;
- merge experimental work into this branch;
- replace the verified receipt path because a newer path appears cleaner;
- treat runtime copies, Downloads copies, chat history, or machine state as authority over this Git reference.

Required response to an attempted alteration:

`ALL_STOP_REFERENCE_LOCK: known-good Brain Buddy baseline is immutable. Create a NEW branch from the referenced SHA or from the last subsequently verified hard stop.`

## Recovery rule

Repository first.

`REFERENCE -> proven receipt -> producing code -> exact SHA -> NEW branch -> reproduce request -> verify returned response -> receipt -> commit -> HARD STOP`

Only after a new implementation has produced a real end-to-end receipt may that new commit become another known-good reference.

## Current proof boundary

The locked baseline proves a direct Gemini request/response receipt path in repository history. It does **not** by itself prove that Gemini or DeepSeek are live right now. Live recovery requires a fresh end-to-end execution receipt.

## Layer law

`WORK -> TEST -> VERIFY -> RECEIPT -> COMMIT -> HARD STOP`

Then:

`TURN AROUND -> reference completed layer -> CREATE NEW BRANCH -> begin next layer`

Never begin the next layer on the completed branch.

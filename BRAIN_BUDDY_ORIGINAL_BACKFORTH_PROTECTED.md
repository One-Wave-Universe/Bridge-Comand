# Brain Buddy — Protected Original Back-and-Forth Baseline

## Status

**PROTECTED / TESTED / DO NOT DEVELOP IN PLACE**

This branch preserves the earliest recovered Brain Buddy Council implementation together with the original Gemini and DeepSeek web bridge set that is actually runnable as a back-and-forth.

## Exact lineage

- Council introduced: `386d5e969c4ecba090f7c7be07252ff74c82911d` — `Recover Brain Buddy Council in Bridge-Comand`
- DeepSeek web bridge restored: `cf02d02f1309e0de933252f9fdaac4d7b6b12da8`
- Gemini web bridge restored: `6bbbf974753ce5a99bd615ea3bdd1d0f58533e59`
- Gemini relay restored / first complete runnable set: `59892c0d171afcfcf2bf9bc4bab0707838db4ca9`

The Council file at 386d5e9 is the original back-and-forth implementation, but that exact commit predates the bridge files it invokes. Therefore 59892c0 is the earliest commit in this lineage containing the Council plus both provider web bridges and Gemini relay required to run it.

## Live verification — 2026-10-02

The exact `59892c0` tree was checked out detached into a temporary worktree and run without modifying its Brain Buddy code.

Command shape:

`python3 brain_buddy/brain_buddy_council.py discussion "<test question>" --rounds 2 --save`

Observed real sequence:

1. Gemini returned a response identifying itself as Gemini Brain Buddy.
2. DeepSeek received Gemini's response in the shared discussion and returned a response identifying itself as DeepSeek Brain Buddy.
3. Gemini received the accumulated Gemini + DeepSeek discussion and returned a second response addressing DeepSeek.
4. DeepSeek received the accumulated second-round discussion and returned a second-round response/tool request.
5. Council completed with exit code 0.
6. Transcript was saved as:
   `External_Work/brain_buddy/outbox/council-discussion-20261002-145100.md`

This verifies the original Gemini <-> DeepSeek discussion/back-and-forth path is operational on the current runtime.

## Immutable protection law

**DO NOT EDIT THIS BRANCH IN PLACE.**

No worker, AI, repair process, experiment, cleanup, refactor, or upgrade may alter this protected baseline.

Any proposed change MUST:

1. start from this protected branch/commit;
2. create a NEW child branch;
3. make exactly the intended change there;
4. run the complete Gemini <-> DeepSeek back-and-forth acceptance test;
5. require real returns from both named providers;
6. preserve the old protected branch regardless of the result;
7. only designate the child as a newer known-good baseline after the full test passes.

A failed or incomplete child branch NEVER replaces this baseline.

## Recovery law

When Brain Buddy breaks:

`PROTECTED BASELINE -> EXACT CODE -> RUN UNCHANGED -> VERIFY BOTH PROVIDERS -> ONLY THEN INVESTIGATE NEWER BRANCHES`

Do not reconstruct Brain Buddy from newer pieces while this protected version exists.

## Acceptance boundary

This test proves the original Council's Gemini/DeepSeek shared-transcript back-and-forth executes end-to-end through both provider bridge paths. It does not automatically prove every later Brain Buddy feature, metadata route, phone route, or newer architectural change.

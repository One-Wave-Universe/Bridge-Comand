---
name: gemini-communication
description: Communicate with Gemini using the One-Wave reference-first protocol. Gemini communication is Jetson-optional; require Jetson only for explicitly machine-local work.
---

# Gemini Communication Skill

## Load first

Before communicating with Gemini, read:
1. `GEMINI_OPTIONAL_EXECUTION_PROTOCOL.md`
2. `METADATA_AND_HANDOFF_CONTRACT.md`
3. `AI_ROUTING.md`
4. the owning project's canonical references required by the task.

For One-Wave Science work, reference the Science repository/canon before asking Gemini. Never substitute bridge documentation for scientific authority.

## Core loop

Always preserve this loop:

`REFERENCE GIT → ASK/PIVOT → REFERENCE METADATA/CENTER-FLIP → VALIDATE/PIVOT → UPDATE GIT/CENTER-FLIP → REFERENCE`

A flip returns through the reference boundary. Do not let an AI answer silently become canon.

## Classify before routing

Choose exactly one execution class.

### reference-only
Use GitHub-visible canon, committed metadata snapshots/manifests, supplied artifacts, and existing references.
Do NOT require Jetson.

### public-data
Retrieve required public sources directly. Preserve source URL, retrieval time, immutable IDs/hashes when available, units, provenance, source class, assumptions and transformations.
Do NOT require Jetson.

### machine-local
Use only when the request actually needs Jetson-local files/cache, GPU/CPU runtime, hardware, or other local machine state.
Jetson may then be required. If unavailable, return BLOCKED under the same request ID. Never invent or silently replace local metadata.

## Build the Gemini request

Preserve one stable request ID.

Include:
- exact question/task;
- canonical repo/ref/path references;
- metadata/source references and hashes;
- assumption/transformation IDs when scientific;
- source class: `real|simulated|test`;
- execution class;
- allowed worker capabilities;
- validation/acceptance criteria;
- unresolved uncertainty.

Never include secrets, tokens, private machine addresses, or unsupported claims.

## Ask

Use any authorized Gemini-capable route that satisfies the execution class.
Do not route through Jetson merely because the worker is Gemini.
Do not stop reference-only/public-data work because Jetson, Hive Pipe, Desktop Commander, SSH, or a local listener is unavailable.

## Validate the response

Bind the response to the same request ID.

Check:
- Gemini actually referenced the requested canon/sources;
- provenance and source class survived;
- assumptions/transformation IDs survived;
- measured facts remain separate from One-Wave interpretation;
- unsupported claims are identified rather than promoted;
- requested acceptance criteria were answered;
- machine-local execution has a matching machine receipt if claimed.

If validation fails, pivot and ask again under the same task lineage. Do not update canon from an unvalidated answer.

## Return/update

Return the validated result to the reference boundary.
Only update Git/project canon when the task authorizes an update.
Record what changed, references used, validation performed, unresolved items, and whether Jetson was used.

## Failure behavior

A dead Jetson is NOT a Gemini communication failure for `reference-only` or `public-data`.
After three equivalent route failures, change route/angle.
A queued request is not execution.
Only matching receipts prove machine execution.

## Fast checklist

`reference → classify → stable ID → ask → metadata reference → validate → return/update → reference`

Default: Jetson optional.

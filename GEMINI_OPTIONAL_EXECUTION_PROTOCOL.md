# Gemini Communication Protocol — Jetson Optional

## Purpose

Gemini communication is a repository/reference protocol. It MUST NOT require the Jetson, Hive Pipe, Desktop Commander, SSH, or any particular machine merely to ask, review, validate, or return an answer.

The Jetson is an optional execution worker for jobs that actually need its local datasets, GPU/CPU runtime, private local metadata cache, or other machine-local resources.

## Reference-first loop

The canonical communication loop is:

`REFERENCE GIT → ASK/PIVOT → REFERENCE METADATA/CENTER-FLIP → VALIDATE/PIVOT → UPDATE GIT/CENTER-FLIP → REFERENCE`

Every handoff preserves one stable request ID and the One-Wave envelope/provenance contract.

## Request

A Gemini request MUST identify:
- stable request ID;
- task/question;
- canonical repo/ref/path inputs;
- metadata references or immutable hashes when required;
- assumption/transformation IDs for scientific work;
- source class `real|simulated|test`;
- whether machine-local execution is actually required;
- allowed optional worker targets;
- acceptance/validation requirements.

No token, credential, or private machine address belongs in the request.

## Execution classes

### reference-only

Use when the answer can be produced from GitHub-visible canon, committed metadata snapshots, supplied artifacts, and public sources.

Jetson availability MUST NOT block this class.

### public-data

Use when additional public metadata is needed. The worker may retrieve public data directly, preserve raw source URLs/retrieval time/hashes, and return references/results under the metadata contract.

Jetson availability MUST NOT block this class.

### machine-local

Use only when the task explicitly requires Jetson-local state, local raw data, GPU/CPU execution, hardware access, or the live `.one-wave-metadata` cache.

If Jetson is unavailable, return a BLOCKED machine-local receipt under the same request ID. Do not silently downgrade to stale or invented metadata.

## Routing

Preferred routing is capability based, not machine based:

1. GitHub/reference-capable Gemini route.
2. Public-data-capable Gemini route when needed.
3. Jetson as an optional worker when machine-local capability is required or intentionally requested.
4. Other authorized workers may satisfy the same envelope if their capabilities meet the request.

A Gemini response is valid because it satisfies the request, provenance, and validation contract—not because it passed through the Jetson.

## Response

A Gemini response MUST bind to the exact request ID and record:
- route/worker;
- canon refs actually read;
- metadata/source refs actually used;
- assumptions/transforms preserved;
- answer/artifacts;
- validation performed;
- unresolved dependencies;
- whether Jetson was used.

For machine-local work, only a matching machine receipt proves execution.

## Metadata portability

Useful bounded metadata required for reference-only work SHOULD be published as provenance-preserving GitHub snapshots/manifests/pointers so phone, Gemini, ChatGPT, and other workers can reason when the Jetson is offline.

Large/raw/private data may remain external or Jetson-local; GitHub stores hashes, manifests, provenance, and authorized pointers rather than secrets or oversized payloads.

## Failure law

A dead Jetson route is not a Gemini communication failure unless the request is explicitly `machine-local`.

Do not queue reference-only work behind an offline Jetson. Switch to a reference/public-data route while preserving the same request ID and canon.

## Compatibility

Existing `jetson-gemini-task.yml` remains a machine-local adapter only. It MUST NOT be treated as the canonical Gemini communication protocol.

Transport metadata authority remains `METADATA_AND_HANDOFF_CONTRACT.md`; scientific meaning remains in the owning Science repository.

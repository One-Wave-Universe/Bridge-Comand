# One-Wave Metadata, Handoff, and Receipt Contract

Bridge-Comand is the authority for transport metadata. Project meaning remains in the owning repo.

## One envelope

Every machine, worker, Foreman, simulator, or AI handoff SHOULD use the same envelope shape:

```json
{
  "schema": "one-wave-envelope/v1",
  "id": "stable-unique-id",
  "kind": "job|command|result|receipt|metadata|artifact",
  "created_at": "RFC3339 timestamp",
  "source": {
    "actor": "chatgpt|claude|codex|deepseek|gemini|foreman|jetson|human|other",
    "machine": "optional hostname/device id",
    "repo": "owner/repo",
    "ref": "branch/tag/commit",
    "path": "optional canonical path"
  },
  "target": {
    "actor": "worker/router/machine",
    "machine": "optional target",
    "repo": "owner/repo"
  },
  "intention": "what is being attempted",
  "consequence": "what may change if it succeeds",
  "canon": ["repo/path@commit-or-ref"],
  "depends_on": ["job-or-envelope-id"],
  "payload": {},
  "limits": {
    "timeout_seconds": 45,
    "max_retries": 3,
    "destructive": false
  },
  "provenance": {
    "source_ids": [],
    "source_urls": [],
    "retrieved_at": null,
    "transform": null,
    "transform_version": null
  }
}
```

Secrets/tokens never go in envelopes committed to git.

## Result / receipt

Execution evidence must bind to the request:

```json
{
  "schema": "one-wave-receipt/v1",
  "request_id": "exact request id",
  "route": "hive-pipe|pull-bridge|actions|remote|adapter",
  "machine": "actual executing machine",
  "started_at": "RFC3339",
  "finished_at": "RFC3339",
  "exit_code": 0,
  "stdout": "...",
  "stderr": "...",
  "artifacts": [],
  "commit_before": null,
  "commit_after": null,
  "receipt_hash": "content hash"
}
```

A branch write, issue, documentation update, queue entry, or worker statement is not a machine-execution receipt.

## Foreman handoff

Foreman job packets additionally carry:
- job ID and lifecycle state;
- owning lane/repo;
- canonical references;
- dependencies;
- acceptance criteria;
- blockers;
- allowed tools/routes;
- expected receipt types;
- claim boundary.

Workers return artifacts + receipts. Foreman validates; workers do not self-promote to DONE.

## Jetson two-state runtime

For the digital brain runtime, add:
- `brain_cycle_id`;
- `state_side: FIELD|VOID|ROUTER`;
- `backend: gpu|cpu|cpu-reference`;
- `source_tag: real|simulated|test`;
- input/output state hashes;
- tolerance/fixture ID for CPU↔GPU comparisons;
- HOLD/ROUTE/STOP resolution;
- retry/depth budget.

GPU/FIELD and CPU/VOID are engineering roles. Metadata must not describe them as experimentally proven physical Field/Void equivalents.

## Public scientific metadata

RAW SOURCE metadata and ONE-WAVE TRANSFORMS are separate stores.

Raw record must preserve:
- provider/dataset;
- immutable provider record ID where available;
- DOI where available;
- source URL;
- retrieval timestamp;
- response/content hash;
- license/usage metadata when available;
- raw payload path.

Transform record must preserve:
- raw source IDs/hashes;
- transform name/version/commit;
- parameters/units;
- output hash/path;
- assumptions;
- uncertainty/null/control metadata;
- validation receipt IDs.

Never overwrite raw data with a transformed interpretation.

## Source classes

`real` = measured/captured external input.
`simulated` = generated sandbox/dream input.
`test` = fixture/synthetic validation input.

Source class must survive routing and compression.

## Failure law

Failures are receipts too. Preserve route, request ID, exit code/error, timestamp, and next allowed route. After three equivalent failures, switch route/angle rather than silently repeating.

# Bridge-Comand disaster recovery

Goal: a bridge failure must degrade to another route, never erase state, and never require guessing.

## Invariants
1. Git is authority for bridge code; runtime machines are replaceable.
2. Credentials never live in git. Recovery checks for their presence but never prints them.
3. Every job has a stable id. Completed ids are idempotent and must not execute twice.
4. Queue transitions are atomic: pending -> processing -> results + done.
5. A stale processing job is recoverable after a lease timeout.
6. No single transport is authoritative. Preferred route failure falls through to the next healthy route.
7. A route is LIVE only after an end-to-end probe returns a matching receipt.
8. Never reset, clean, force-push, delete credentials, or overwrite a working checkout during automatic repair.

## Recovery order
REFERENCE GIT -> REFERENCE METADATA -> VALIDATE -> RETURN TO REFERENCE/UPDATE.

Transport ladder:
1. local/authorized terminal route
2. Hive Pipe gateway
3. pull worker
4. GitHub Actions/queue relay
5. manual recovery command

A failed layer records why it failed and advances. It does not loop forever on one broken route.

## Cold rebuild
Clone Bridge-Comand into a fresh directory. Run `hive-pipe/bridge_doctor.py`. Restore secrets from the machine's secret store/environment, not from git. Install services from repo scripts. Run `hive-pipe/bridge_doctor.py --probe`. Only declare recovery after the probe receipt says PASS.

## Power/network interruption
Jobs remain files, not memory-only state. On startup, recover stale processing jobs, preserve existing results, then resume pending work. Never re-run an id with an existing result/done marker.

## Required backups
Keep three independent things: GitHub repository, one local checkout, and one exported secret/recovery record stored outside the repo. The secret backup must not contain ordinary project source as its only copy.

# One-Wave Device Lattice

**Canonical device-routing topology**

## Nodes

- PHONE — control/client endpoint
- LAPTOP — control + worker/execution endpoint
- JETSON — worker/execution endpoint
- GITHUB — durable public control plane, queue, Actions and receipt surface

## Required logical pathways

```
PHONE  ⇄ GITHUB ⇄ LAPTOP
PHONE  ⇄ GITHUB ⇄ JETSON
LAPTOP ⇄ GITHUB ⇄ JETSON

PHONE  ⇄ GITHUB ⇄ LAPTOP ⇄ JETSON
PHONE  ⇄ GITHUB ⇄ JETSON ⇄ LAPTOP
```

Direct LAN/Hive-Pipe/remote routes may shorten a path when live, but the GitHub path remains the durable fallback/control plane.

## Routing law

Every node advertises:
- stable node ID;
- capabilities;
- allowed operations;
- route health;
- last receipt time;
- source class;
- current project/canon refs where relevant.

Every routed request preserves:
- request ID/idempotency key;
- source node;
- target node;
- intention/consequence;
- bounded command/job;
- permissions/limits;
- canon + assumption/transformation IDs where applicable;
- provenance;
- hop list;
- receipt chain.

## Open means routable, not unauthenticated

“All lattice pathways open” means any authorized node may address another through an available route. It does not mean exposing arbitrary public shell access.

Machine execution remains authenticated and bounded. Tokens/secrets never travel in committed envelopes.

## Failover

For each source→target request:
1. select healthy direct route if available;
2. otherwise GitHub control plane;
3. otherwise durable GitHub/store-and-forward queue;
4. preserve failure receipt and retry/switch route;
5. after three equivalent failures switch angle/route rather than repeat blindly.

No route may substitute an old receipt for the current request.

## Hop receipts

Each hop appends, never rewrites:
`source → route → target → started → finished → status → receipt/hash`

End-to-end success requires the final target receipt matching the original request ID.

## Laptop execution

Laptop is a first-class worker, not merely a UI. GitHub-originated jobs may target LAPTOP when its authenticated worker/gateway is live. A phone can therefore originate work for the laptop without LAN proximity.

## Jetson execution

Jetson remains a first-class compute/worker node. Phone or laptop can originate its jobs through GitHub.

## Cross-machine work

A job may explicitly route:
`PHONE → GITHUB → LAPTOP → JETSON`
or
`PHONE → GITHUB → JETSON → LAPTOP`
when the job contract requires both machines. Each machine emits its own hop receipt.

## Acceptance

The lattice is not fully proven until harmless probes produce matching end-to-end receipts for:
- phone→GitHub→laptop;
- phone→GitHub→Jetson;
- laptop→GitHub→Jetson;
- Jetson→GitHub→laptop;
- suspend/resume without duplicate execution;
- one endpoint offline with queued recovery;
- rejected unauthorized request;
- preserved assumption/transformation/provenance metadata across hops.

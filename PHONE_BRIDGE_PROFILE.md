# Phone Bridge Profile

**Target:** Android/mobile clients, including browser/PWA-style control surfaces.

The phone is a client and relay endpoint for the same One-Wave envelope/receipt contracts. It does not get a separate scientific or project authority.

## Mobile constraints

Never require the phone client to have:
- direct localhost access to the Jetson;
- SSH or a shell;
- a continuously alive background process;
- an inbound listening port;
- a stable LAN address;
- large repository checkouts.

Prefer outbound HTTPS. Use WSS only when a live stream materially helps. The durable fallback is store-and-forward request/receipt polling.

## Required mobile operations

1. Fetch bridge/Foreman status.
2. Submit a bounded job/command envelope.
3. Receive a stable request ID immediately.
4. Poll/fetch the matching receipt later.
5. Resume after app/browser suspension without duplicating execution.
6. View stdout/stderr/status/artifact references in bounded chunks.
7. Cancel a queued/not-started request where the route supports it.
8. Never expose credentials in committed payloads or UI logs.

## Idempotency and resume

Every submitted action uses a stable request ID/idempotency key.

Reconnect behavior:
- client resends/fetches by request ID;
- server/relay returns existing state rather than executing a duplicate;
- QUEUED, RUNNING, SUCCEEDED, FAILED, CANCELLED are transport states;
- scientific validation status remains separate.

## Small-envelope rule

Mobile control messages SHOULD remain small. Large logs, datasets, images, models and artifacts are referenced by content hash + authorized location and fetched separately/ranged.

## Route preference

PHONE
→ outbound HTTPS gateway
→ authenticated bridge/router
→ Foreman/worker/Jetson route
→ matching receipt
→ HTTPS receipt/status fetch

If the live gateway is unavailable:
PHONE → durable queue → later worker pickup → receipt store → phone fetch.

## Source/provenance

Phone-originated sensor captures or files must preserve:
- source_tag real|simulated|test;
- device/client identifier that does not expose unnecessary personal data;
- capture timestamp and timezone/clock metadata;
- content hash;
- MIME/schema;
- units/calibration where scientific;
- assumption/transformation IDs when applicable.

## Security boundary

No arbitrary unauthenticated command endpoint.
The phone submits bounded envelopes; the machine-side router enforces permissions, limits, canon, and destructive-action policy.
Tokens live in platform credential storage/session secrets, never git.

## Acceptance tests

A phone bridge is not considered working until receipts show:
- submit from mobile network/Wi-Fi independent of Jetson LAN;
- suspend client, resume, fetch same request without duplicate execution;
- gateway disconnect/reconnect;
- failed request preserved as receipt;
- small status/receipt rendering;
- authentication rejection fixture;
- same envelope accepted from desktop and phone;
- exact request ID reaches machine receipt.

Documentation or a deployed endpoint alone is not proof.

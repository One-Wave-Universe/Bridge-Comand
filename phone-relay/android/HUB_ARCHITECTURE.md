# One-Wave Phone Communication Hub

The phone is a durable local communication/control node.

Stores: `inbox/`, `outbox/`, `receipts/`, and `references/`.
Secrets are separate in an Android Keystore-backed encrypted vault.

Secret values never enter Git commits, request/reference envelopes, hub JSON,
receipts, or status/log output.

Route:
`AI/client -> PHONE HUB -> route -> AI/client -> PHONE HUB -> verified receipt`

Transport parser remains two-state: `REQUEST -> RESPONSE`. Delivery status is
separate from reasoning state.

Future route adapters can use direct HTTPS APIs, Android shares, GitHub, Hive
Pipe, or other workers without changing the hub contract.

A route is proven only by a real matching response receipt.

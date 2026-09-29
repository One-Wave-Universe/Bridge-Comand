# Phone AI Relay

This fills the missing mobile parser/worker between AI clients without making
the Jetson part of the live message path.

## Route

`ChatGPT -> phone share -> Gemini -> phone share -> ChatGPT`

GitHub supplies durable references/receipts. The phone is a relay endpoint.
The worker has two states only: `REQUEST -> RESPONSE`.

It does **not** claim to remotely control either app. Android's normal share
surface is the transport. The same request ID survives both pivots.

## Request

See `request.example.json`.

Generate the outbound handoff:

```bash
python3 phone-relay/relay_worker.py handoff phone-relay/request.example.json -o /tmp/handoff.json
```

Share the resulting `share_text` to the target AI.

When the target replies, save/share the complete returned text and parse it:

```bash
python3 phone-relay/relay_worker.py receipt phone-relay/request.example.json response.txt -o receipt.json
```

A response is rejected unless it contains the exact matching request ID.

## Acceptance

The bridge is proven only when a real target AI returns the matching request ID
and its actual response is captured in a receipt. A generated handoff alone is
not success.

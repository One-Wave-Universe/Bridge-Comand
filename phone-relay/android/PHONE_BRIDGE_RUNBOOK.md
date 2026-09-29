# Phone Bridge Runbook

The Android phone is an independent bridge node, not a UI-only helper.

## Center/reference
Every route starts and ends at the same request ID + reference. The phone stores inbox, outbox, receipts, references, and route health locally. Credentials remain only in the encrypted Android vault.

## Routes
1. direct provider HTTPS (Gemini implemented);
2. GitHub Actions control/reference lane;
3. Android share fallback;
4. Jetson/Hive Pipe only after a reachable Jetson edge exists.

Route health is hysteretic: success reinforces a route; failure decays it. A failed edge returns to center and another route may be selected. Do not erase a route after one failure.

## GitHub phone edge
Store a fine-grained GitHub token in the phone vault as GITHUB_TOKEN. Minimum permission depends on operation; workflow dispatch requires Actions write permission. Do not commit the token.

Phone dispatch target is One-Wave-Universe/Bridge-Comand on main. A dispatch receipt means GitHub accepted the request; it does NOT prove the downstream Jetson/provider endpoint succeeded. Poll/read the resulting workflow receipt before promoting the downstream route to healthy.

## Acceptance
PHONE -> route -> target -> matching response/receipt -> PHONE.
Each layer has its own state: accepted, running, completed, endpoint-verified.
Only endpoint-verified strengthens the complete path.

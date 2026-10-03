# Repo Lens verification — 2026-10-03

This is a software/transport receipt, not scientific proof or a physical-cell measurement.

## Full repository and peer exchange

[Actual run](https://github.com/One-Wave-Universe/Builds/actions/runs/37123204993): request `council-independent-jetson-pieces-20261003-01` on Builds branch `feature/repo-lens-deepseek-jetson-20261003`.

All completed turns used Builds main `b0e8cb7e8779ac19e327b86d2b9ef9341cec57a9`: 197 tracked files fetched and hash-verified, every UTF-8 text supplied in five segments. Binary bytes were verified, not semantically interpreted. CERN CMS and GWOSC observing-run metadata were retrieved on Jetson and preserved as provider JSON with URL, time, bytes and hash.

Gemini completed cycle 1 after receiving the previously completed GPT receipt. GPT completed cycles 1 and 2 after receiving Gemini's actual cycle 1 answer. GPT corrected Gemini's description of GWOSC run bounds as event-trigger boundaries. Gemini hit quota on its second cycle; GPT still finished its second cycle. The overall request correctly ended PARTIAL.

GPT synthesis receipts: `01a101c1-b51d-7b30-ae50-db205c61f977`, `01a101c3-660d-7cc2-a249-a30d16ed7129`. Gemini receipt: `A_bAatyTPJfWjMcPl7fLuQg`.

## Piece delivery and route boundaries

DeepSeek uses smaller 6000-character source segments, per-segment progress and bounded findings reduction. Every segment must succeed before full reference can complete; no failed piece is silently omitted. The app displays pieces read and defaults to the supported maximum of 256 model calls per cycle. Larger repositories may still exceed this budget and must stop explicitly.

DeepSeek's free Firefox transport returned matching short markers earlier, but the full-repository requests failed. The latest full request returned HTTP 400 before a completed segment. A separate multiline marker test returned upstream HTTP 500 after 120 seconds. This route is NOT full-loop verified. The Dell relay health endpoint responds, while its Commander registrations are offline and SSH/Hive control routes were unavailable at inspection.

Claude's official client is installed and its adapter is prepared; account sign-in remains incomplete. Grok's adapter is prepared but no authenticated route is configured. Neither has a verified model response. Their failures did not stop GPT.

## Published app

[Repo Lens](https://repo-lens-adlard.markluvsoliviaduh.chatgpt.site) source `28e54b8aad85957870765b4d994a19cb0b195af8`, private deployment `appgdep_6ac0f832ec6c81918de916097694e57d`, succeeded with MCP enabled. Submission/authentication tests, build and artifact validation passed. The default result is the actual independent council request above.

Bootstrap reads fresh GitHub authority, complete manifests and terminal/metadata tool routes. It is explicitly not full content coverage; the runner enforces the full scan. Providing this bridge does not establish that every AI client has installed or connected the MCP plugin.

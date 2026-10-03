# Live DeepSeek input repair — 2026-10-03

Dell Desktop Commander reconnected after the user's laptop restart as device `6d4b6585-ca68-4c8b-a3f1-52f64a92c07d`. Target identity: `scales-Latitude-E7450`, user `scales`; free disk space 64 GB.

The actual runtime source `/home/scales/.local/state/one-wave-deepseek-web/deepseek_web_relay.py` was inspected (SHA-256 `0fc4002d84ff405482006153fee39dfd832bdb41a69bb414c451af98bd00f4c5`). Only prompt entry and the partial-timeout fallback changed. Its original source is preserved as `deepseek_web_relay.before-repo-lens-input-repair.py`; no browser profile or repository was copied. Patched source SHA-256: `12700aeeecfe8a697bf063f5e3b7fe5f2df6bc3cba0ea4cbfcbaba70a19dd913`.

All three input regression tests passed on the Dell. Only `one-wave-deepseek-web-relay.service` was restarted, exit 0, and returned active.

Actual free-web responses through the existing Jetson gateway:

- Real Builds `digital-cell/l0_cell.py` reference, 2007 prompt characters: exact marker `DEEPSEEK_REAL_REPO_PIECE_OK_20261003`, response `webrelay-9dba9efa866d47f1833d7ef7637011f4`, 6.00 seconds.
- Deliberately repeated code as a transport stress test, 32438 prompt characters: exact marker `DEEPSEEK_32K_PIECE_OK_20261003`, response `webrelay-8f4e6801fec14eb99985344b99f611e8`, 5.43 seconds. This is a transport test, not full repository coverage.

Builds runner commit `5dc2af592a37fb44db488f2011d1e1c65f761247` uses 24000-character source pieces and a total 32000-character DeepSeek packet guard. All 15 runner regressions passed before publication. Other providers and mains were unchanged.

One bounded full-repository verification was submitted: `deepseek-repaired-full-builds-20261003-01`, one DeepSeek cycle, maximum 64 model calls, unchanged CERN/GWOSC source metadata and actual prior GPT/Gemini peers. Its result is pending until the full scan, all source pieces, peer reading, final synthesis and HEAD drift check complete. Do not infer success from either marker. The inherited stable-text completion heuristic remains a limitation of this browser transport.

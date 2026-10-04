# Pull relay recovery — 2026-10-04

Owning repo: One-Wave-Universe/Bridge-Comand.
MAIN GOAL: reliable two-state request/return relay with current target receipts.
WHY: Grok has no direct device tools; Actions lacks gateway secrets; published pull returns were stale.
REFERENCE: base f46375f3dbedccc6f6097b93ca3ff21d5ef194c3; actual Jetson canonical Bridge-Comand feature branch e323af0e585a58cc70d452406ede668db0587ce7 (untracked bytecode only); project /home/Scales/One-Wave-Science on recovery branch preserved.
ACTIVE TASK: fix/pull-read-write-isolation-20261004, /tmp/bridge-pull-fix-20261004.
EXACT CHANGE: independent inbound/outbound backoff; exact-ID/digest published-return reconciliation; archive stale reply instead of replacing current; explicit runtime module and transport roots.
ALLOWED FILES: chatgpt_terminal_pull.py, test_pull_transport_isolation.py, this receipt and canonical operations pointer.
PROTECTED: existing user branches, Science dirty work, credentials, parser boundaries.
TESTS: nine unittest failure/recovery controls pass (Jetson process 1760512); existing parser_relay check passes (1762856); Python compile/diff checks pass.
ATTEMPT: 1/3 software approach; all regression controls pass.
OBSERVED FAILURE: failed old-result git pushes consumed both transport routes' backoff before new-request polling. gh auth status shows no GitHub login; Actions secrets absent per user run.
DIRECT RECOVERY: grok-terminal-20261004-1143 executed through the bounded parser using the Science project root, exit 0: Scales / localhost.localdomain / /home/Scales/One-Wave-Science.
RETURN: published on both Science transport branches through the authenticated GitHub connector; archived .chatgpt-terminal/results/grok-terminal-20261004-1143.json.
LIVE DEPLOYMENT: user-service drop-in 50-poll-delivery-isolation.conf points at explicit runtime cache ~/.local/state/one-wave-chatgpt-terminal/runtime/6b0ea1b144a1a558864b2f92a7b364b22ebfae07/chatgpt_terminal_pull.py. Canonical Bridge-Comand supplies shared modules and transport remote; Science remains the bounded project root. Existing source checkouts were not switched/reset.
SERVICE: one-wave-chatgpt-terminal-pull.service restarted and active; no credentials created/exposed.
AUTONOMOUS INTAKE PROOF: pull-recovery-proof-20261004-1153 picked up by the background worker, printed PULL_WORKER_RECOVERY_OK, exit 0, completed 2026-10-04T18:53:24.535960+00:00. Read-route counters stayed healthy despite outbound auth backoff.
RETURN PROOF: exact worker receipt published and read back on both transport branches through the connector; digest cd0332b1084720e6486cd01166e8c31f7b2159d3dbbdf13d79bca0eb5599f097.
FIELD NOTES: active service is not end-to-end route proof. The corrected client guide cannot create tools in Grok's session.
VOID OVERSIGHT: deterministic code/tests/target receipts support intake recovery; outbound git push remains BLOCKED, not healthy.
PROGRESS: request execution and connector-assisted return TESTED; unattended complete relay PARTIAL.
LOOK-BACK: separated execution from delivery and inbound/outbound transport state. A completed ID reconciles through its matching return; old replies cannot overwrite newer ones.
HARD STOP: tested fix, deployed intake, exact published receipts; no all-routes-live claim.
HANDOFF: establish authorized GitHub write identity on target or a configured autonomous authenticated return relay. Actions requires its own missing URL/token configuration separately.
ROLLBACK: remove only the new service drop-in, daemon-reload and restart to restore the original unit. Runtime cache is a pinned execution artifact, not competing repository authority.
CONTRIBUTION: Codex, deterministic CPU tests and real Jetson execution.

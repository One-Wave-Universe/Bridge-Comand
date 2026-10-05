# AI scientific metadata relay

Transport authority: Bridge-Comand. Archive registry, AI acquisition commands, dependency environment and interpretation rules remain in One-Wave-Science/JETSON_SCIENCE_ARCHIVE_ROUTES.md. Particle/measurement mapping lives in One-Wave-Science/Engine/PARTICLE_TO_WAVE_CONVERSION_CHART.md. Initial implementation and matching receipt: https://github.com/One-Wave-Universe/One-Wave-Science/pull/210 . Refresh those canonical references before each action; never maintain a second registry here.

Resolve the actual Jetson, canonical Science root or authorized task worktree, branch, HEAD and working-tree status. Prefer the available direct device terminal. The existing authenticated Hive Pipe terminal_run can relay the same commands; choose the current configured gateway rather than a remembered tunnel URL.

Example terminal_run arguments, after substituting the verified cwd:

```json
{
  "argv": ["python3", "scripts/science_archive_search.py", "openneuro", "--record", "ds000224", "--output", ".one-wave-metadata/current/openneuro"],
  "cwd": "/verified/Science/checkout",
  "timeout": 45,
  "intention": "Retrieve public brain-scan archive metadata required by the named repository question.",
  "consequence": "Retain raw provider response, identifiers and SHA-256 receipt only; do not modify solver equations or infer physical waveforms from metadata."
}
```

Use a fresh JSON-RPC request ID, keep authentication outside git, require the same returned ID and actual exit code, then inspect source record IDs, timestamp, hash and receipt. The Science route document gives CERN, GWOSC, MAST, HEASARC, Gaia, ESO, ALMA, DESI, OpenNeuro, DANDI and EEG commands and their verified scope. For native telescope queries use the user-local pinned Python environment named there.

Verified 2026-10-05: direct Jetson metadata calls and authenticated local Hive Pipe MCP terminal_run returned a matching request ID and exit 0 for GWOSC. External HTTPS tunnel was not separately tested. HEPData public search/record requests returned 403; retain BLOCKED and do not invent substitute data. Detailed source statuses belong to the canonical Science receipt, not this transport pointer.

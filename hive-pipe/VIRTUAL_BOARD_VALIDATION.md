# Hive Pipe add-on: Virtual Breadboard / Perfboard validation

**Audience:** hive-pipe agents, bridge clients, and humans validating circuits/builds before claiming pass.

**Canonical simulator home (prefer this):**  
`https://github.com/One-Wave-Universe/Builds/tree/main/Virtual_Breadboard`

Older copies under `One-Wave-Science/Virtual_Breadboard` are legacy. Do not treat Science as the authority for board layout, `simulate.js`, or receipts once Builds has the tree.

Related hive notes: [`BRIDGE_DIRECTIONS.md`](BRIDGE_DIRECTIONS.md), [`README.md`](README.md).  
Related Builds contracts:  
[`BENCH_REALITY_CONTRACT.md`](https://github.com/One-Wave-Universe/Builds/blob/main/Virtual_Breadboard/BENCH_REALITY_CONTRACT.md),  
[`AI_COLLABORATION.md`](https://github.com/One-Wave-Universe/Builds/blob/main/Virtual_Breadboard/AI_COLLABORATION.md),  
[`10_RECEIPTS/README.md`](https://github.com/One-Wave-Universe/Builds/blob/main/Virtual_Breadboard/10_RECEIPTS/README.md).

---

## 1. When to use breadboard vs perfboard

Both boards share the **same** Circuit JSON, `js/circuit.js` MNA solver, parts palette, and receipt schema. Only the **physical nets** differ.

| Use | Board | Why |
|---|---|---|
| Student / strip-rail practice, quick prototypes, CELL_V1 copper strip experiments | **Virtual Breadboard** (`layout`: `1large`, `2small`, …) | Columns merge a–e and f–j; power rails are continuous strips — matches a real solderless breadboard. |
| Point-to-point / permanent-layout rehearsal, no accidental strip shorts, “every hole is its own pad” | **Virtual Perfboard** (`kind: 'perf'` / layout keys `1perf`, `1perf-small` when presets are merged) | Each pad is its own `cellId`. Nets merge **only** where you place jumpers/wires. Matches a real perfboard. |
| Magnetic / remanence / Cell-0 physical claim | Neither alone | Sim can give **MODELED** / **SOLVER PASS** / **MODEL PASS**. **PHYSICAL PASS** still needs bench `LOG.md` / measured receipts. |

**Rule:** pick the board that matches the **physical** topology you intend to build. Do not validate a perfboard wiring plan on strip-merged breadboard nets (or the reverse) and call it the same build.

Perfboard status note: pad-isolation lives on Builds branch work / `feat/virtual-perfboard-layout` (Science legacy). Until `1perf` presets are on `main`, use:

```js
Board.build([{ size: 'large', kind: 'perf' }])
```

or Circuit JSON with `"layout": "1perf"` only after presets land in `js/app.js` and `simulate.js`.

---

## 2. Where to run it (human and AI)

From a Builds checkout:

```bash
cd Virtual_Breadboard
# optional: npm install   # needed for Electron / some scripts; node tests often run without

# Headless — preferred hive / AI path
node simulate.js experiments/brain_cell_001.json
# or pipe JSON:
printf '%s' "$CIRCUIT_JSON" | node simulate.js

# Tests / receipts
npm test
npm run receipts   # or: node 10_RECEIPTS/generate_receipts.js

# UI
# open index.html in a browser, or npm start / desktop AppImage when packaged
```

**Hive Pipe route:** use an authorized terminal/Python tool with cwd under the Builds checkout (or an allowed work root that contains it). Example intention: “Validate circuit X on Virtual Breadboard via simulate.js”; consequence: “Expect JSON receipt with status and exit 0 if solve completed.”

Do **not** invent success from docs. A live validate needs stdout/stderr/exit (or a saved receipt file) from that run.

**Browser API (same engine):**

```js
window.breadboard.load(spec)   // places parts
window.breadboard.run(0.05, 0.001)
window.breadboard.receipt()    // status: UNRUN | EDITED_PENDING | MODELED
```

**Ask AI / explore loop (UI):** build → short solve → summarize receipt → if unhealthy, adjust → retest (see `js/ai-explore.js` / Ask AI). Offline templates exist for LED/divider/RC when no API key.

---

## 3. Circuit JSON shape (minimum)

```json
{
  "layout": "1large",
  "parts": [
    { "type": "battery", "id": "V1", "value": 5, "a": { "row": "+", "col": 1 }, "b": { "row": "-", "col": 1 } },
    { "type": "resistor", "id": "R1", "value": 220, "a": { "row": "a", "col": 5 }, "b": { "row": "a", "col": 10 } },
    { "type": "led", "id": "D1", "color": "red", "a": { "row": "a", "col": 10 }, "b": { "row": "-", "col": 10 } }
  ],
  "sim": { "seconds": 0.05, "dt": 0.001 }
}
```

- Hole refs: `{ "row", "col", "board"? }` — must land on the **current** layout.
- CLI-only part types / sweeps (`sim`, `experiment`, `sweep`, `monteCarlo`, `diffsource`, …): use `simulate.js`, not the editor import path alone.
- For perfboard, every connection you need must be an explicit wire/jumper; adjacent pads are **not** pre-tied.

---

## 4. AI validate loop (build → test → receipt → adjust)

Hive / board AI should treat validation as a loop, not a one-shot place:

1. **Build** — emit Circuit JSON; `load` / `simulate.js` with the correct `layout` / `kind`.
2. **Test** — fixed-duration run (`sim.seconds` / `sim.dt` or `window.breadboard.run`). Prefer fixed step over live frame timing for receipts.
3. **Receipt** — capture JSON (`Measure / receipt`, `.receipt()`, or CLI stdout). Keep `schema: virtual-breadboard-receipt/v1`.
4. **Judge** — see §5. If warnings, non-convergence, missing source current, or wrong topology: **adjust** parts/wiring (not the PASS vocabulary).
5. **Retest** — reload adjusted JSON; new receipt. Cap retries (UI explore loop typically ≤2 automatic repairs; hive agents may explore further but must attach every receipt).
6. **Hand off** — attach the last receipt + Circuit JSON to the hive job. Preserve source class `simulated` (or `test`). Do not self-promote Foreman jobs to DONE from a modeled receipt alone.

Protected: hive-pipe agents must not wipe or rewrite `Virtual_Breadboard/**` as a side effect of a queue step unless that file change is the explicit authorized task.

---

## 5. What counts as PASS vs MODELED

Receipt / UI statuses (editor):

| Status | Meaning |
|---|---|
| `UNRUN` | Spec loaded or idle; no successful solve for this state yet. |
| `EDITED_PENDING` | Board changed; old numbers withheld until next solve. |
| `MODELED` | Solver produced numbers for the **model**. **Not** a physical or bench pass. |

Qualification ladder ([`BENCH_REALITY_CONTRACT.md`](https://github.com/One-Wave-Universe/Builds/blob/main/Virtual_Breadboard/BENCH_REALITY_CONTRACT.md) §9) — use these words literally:

| Claim | Requires |
|---|---|
| **SOLVER PASS** | Equations solved; numeric thresholds of that test met. |
| **MODEL PASS** | Expected behavior in the modeled components (plus SOLVER PASS). |
| **BENCH-REALITY PASS** | Also passes bench-reality audit (supply / 0-spine / drive / current limit / return topology match the intended physical build). |
| **PHYSICAL PASS** | Measured on actual hardware (bench log, not only sim). |

**Hard rules for hive language:**

- `MODELED` ≠ PASS. Never say “passed” for a receipt that only says `MODELED`.
- No warnings ≠ safety, frequency fidelity, energy closure, or bench qualification.
- Magnetic / remanence / Cell-0: electrical CELL_V1 sims can be MODEL/SOLVER pass; B-field / remanence claims stay **MODELED** or experiment until PHYSICAL PASS.
- Source current: if loads dissipate power, a display of `0.00 A` without a real solved source current is not acceptable for BENCH-REALITY PASS (F0 limit example: `|I_source| ≤ 20 mA` is an acceptance limit, not proof of physics alone).

Committed regression green (`npm test`, `test/regression-builds/`) proves the **engine and fixtures**, not that today’s custom circuit is bench-qualified. Per-run receipts under `10_RECEIPTS/current|passing|failing/` are ephemeral snapshots (`npm run receipts`).

---

## 6. Minimal hive checklist

```text
[ ] Checkout / cwd is Builds/Virtual_Breadboard (not an abandoned Science copy)
[ ] Board kind matches physical intent (breadboard strips vs perf pads)
[ ] Circuit JSON validated / loaded without “Unknown layout”
[ ] Fixed-duration solve completed (exit 0 or receipt with nodes/branches)
[ ] Status recorded honestly: MODELED vs SOLVER/MODEL/BENCH-REALITY/PHYSICAL PASS
[ ] Receipt + spec attached to the job; source class = simulated|test
[ ] No claim of PHYSICAL PASS without hardware log
```

---

## 7. Pointers

- Desktop / install notes: `Virtual_Breadboard/INSTALL_UBUNTU.md`, README “Programs” section when present.
- Practice / AI API: README “Repeatable human / AI practice”.
- Perfboard net rules: `02_CONNECTIONS/MAP.md` (and perfboard branch docs when merging).

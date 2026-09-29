# Jetson Gemini Dispatch

Canonical primary Gemini worker path:

task packet (paths only) -> GitHub Jetson Command Lane -> Hive Pipe terminal_run -> Jetson One-Wave-Science checkout -> scripts/gemini_min.sh -> official Gemini CLI -> matching machine/provider output.

The direct Gemini API/evidence-pack lane is an independent reviewer/fallback and MUST NOT be represented as Jetson Gemini execution.

## Dispatch contract

Working directory:
`/home/Scales/One-Wave-Science`

Review argv:
`["bash","scripts/gemini_min.sh","review","tasks/gemini/<task>.md"]`

Smoke argv:
`["bash","scripts/gemini_min.sh","ask","Reply with only: GEMINI JETSON OK"]`

A dispatch is not proof. A green configuration check is not proof. Accept Jetson Gemini execution only when the Jetson Command Lane returns the terminal_run result for the requested argv with exit code 0 and Gemini JSON output attributable to the same invocation.

Task packets:
- contain paths, questions, constraints and acceptance criteria;
- do not paste repository trees or large source files;
- stay within gemini_min.sh's bounded packet limit;
- never contain credentials.

Gemini CLI reads the named paths from the Jetson checkout and may follow only the smallest direct dependencies allowed by the task.

## Current engine task
`tasks/gemini/physics-engine-foundation-001.md`

Expected argv:
`["bash","scripts/gemini_min.sh","review","tasks/gemini/physics-engine-foundation-001.md"]`

Expected cwd:
`/home/Scales/One-Wave-Science`

If the gateway/tunnel is unavailable, preserve the task and failed route receipt. Do not substitute an API answer as a Jetson receipt.

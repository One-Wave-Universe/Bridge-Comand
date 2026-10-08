# Bridge-Comand — bridges and machine access

## Start here — table of contents

Choose a subject below. Folder links show their contents; README and guide links explain how to use them. A source-code page is not a launched app. Read each program's launch instructions before trying to run it on a phone or computer.

| What you need | Open | What it is |
|---|---|---|
| Read first | [BRIDGE_COMMAND_START_HERE.md](BRIDGE_COMMAND_START_HERE.md) | Canonical bridge contracts, operations and dated receipts |
| Hive Pipe | [hive-pipe/README.md](hive-pipe/README.md) | Main bridge implementation and usage |
| Bridge directions | [hive-pipe/BRIDGE_DIRECTIONS.md](hive-pipe/BRIDGE_DIRECTIONS.md) | Bridge operating directions |
| Laptop access | [hive-pipe/SHARED_LAPTOP_ACCESS.md](hive-pipe/SHARED_LAPTOP_ACCESS.md) | Laptop relay instructions |
| Recovery | [DISASTER_RECOVERY.md](DISASTER_RECOVERY.md) | Recovery entrypoint |
| Science archive relay | [SCIENCE_ARCHIVE_RELAY.md](SCIENCE_ARCHIVE_RELAY.md) | External science-data transport |
| Active GitHub workflows | [.github/workflows/](.github/workflows/) | Workflows GitHub Actions discovers |
| Other workflow files | [workflows/](workflows/) | Additional workflow files; presence here does not establish activation |
| Folder watchers | [hive-pipe/OWATCH_FOLDER_TYPE.md](hive-pipe/OWATCH_FOLDER_TYPE.md) | Folder watcher conventions |
| Bridge mesh | [hive-pipe/MODULAR_HYSTERETIC_BRIDGE_MESH.md](hive-pipe/MODULAR_HYSTERETIC_BRIDGE_MESH.md) | Bridge route architecture |
| Pull recovery receipt | [hive-pipe/PULL_RECOVERY_2026-10-04.md](hive-pipe/PULL_RECOVERY_2026-10-04.md) | Dated evidence and remaining authentication boundaries |

## How to organize, clean, build, work and decide

1. **Find the owner.** Use the repository table below and the canonical routing map before creating a file. Put science in Science, build artifacts in Builds, fiction in Mythos, and transport in Bridge-Comand. Link to the owning file rather than maintaining another copy.
2. **Reference before work.** Read this table of contents, the relevant project guide, current status and applicable rules. Verify repository, branch and commit. Old chats and old receipts are context; current authoritative files decide the task.
3. **Decide one next step.** State the goal, what already works, the smallest remaining gap, the files allowed to change, the expected result and the check that would prove it. Keep hypotheses separate from measurements and tested behavior.
4. **Work on a task branch.** Inspect existing changes first. Make one bounded change, preserve unrelated work, and use a pull request. Follow the [canonical branch and receipt rules](https://github.com/One-Wave-Universe/One-Wave-Science/blob/main/GENERAL_REFERENCE_RULES.md).
5. **Build or run from the project guide.** Open the project's README or launch instructions and use its stated dependencies, commands and tests. Documentation, source files and queued jobs do not prove that a program runs. Phone support must be checked for the actual app.
6. **Check the result.** Inspect the exact diff, run the relevant checks, and record actual output and unresolved gaps. For bridges, require a matching end-to-end receipt. For science, use source-backed evidence and current metadata; for hardware, require measurements for physical claims.
7. **Clean deliberately.** Identify the canonical source before removing a duplicate. Preserve unique content and user work; repair links when relocating files; check incoming references before deletion. Do not bulk-delete unfamiliar files or create a new permanent repo copy to make navigation easier. Cleanup requiring a move or deletion gets its own bounded task.
8. **Close and update navigation.** Record what changed, what passed, what failed and the next smallest step in the owning project's existing status/receipt records. When adding, moving or retiring a project, update its README and this table of contents in the same change. Keep detailed rules in their owning authority and link to them here.

### Navigation appendix: what the labels mean

| Label | Meaning |
|---|---|
| README / Start here | Entry instructions and navigation |
| Rules / Canon | Constraints and authoritative instructions |
| Map / Index | Where subjects live and how they connect |
| Status / Work order | Recorded progress, gaps and priorities |
| Source / App folder | Implementation; consult its launch instructions |
| Tests / Validators | Checks and reproducible verification |
| Receipt / Audit | Evidence of a specific operation or review |
| Migration map | Placement destinations; not proof a move has happened |
| Hypothesis | Proposed mechanism awaiting the stated evidence |

## Where things belong

| Repository | What belongs there |
|---|---|
| [Builds](https://github.com/One-Wave-Universe/Builds) | Build artifacts, hardware, CAD, editors and runnable build tools |
| [One-Wave Science](https://github.com/One-Wave-Universe/One-Wave-Science) | Scientific models, hypotheses, equations, evidence, research books and science posters |
| [Mythos and Stories](https://github.com/One-Wave-Universe/Mythos-and-Stories) | Fiction, creative stories and narrative books |
| [Bridge-Comand](https://github.com/One-Wave-Universe/Bridge-Comand) | Machine access, bridges, relays and AI transport |

The [canonical organization map](https://github.com/One-Wave-Universe/Builds/blob/main/ALL_GITHUB_INTO_THREE.md) and [routing map](https://github.com/One-Wave-Universe/Builds/blob/main/MIGRATION_MAP.md) own cross-repository placement. Existing files may still await migration; a link describes their current location, not completed relocation.

## Navigation appendix

Use the table above for current paths. Bridge contracts remain in [the canonical start guide](BRIDGE_COMMAND_START_HERE.md); scientific interpretation belongs to Science and build artifacts belong to Builds. Dated receipts prove only the operation they recorded, not present route health.

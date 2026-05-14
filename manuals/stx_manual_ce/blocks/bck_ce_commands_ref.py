"""CE Manual — Part 5: Commands Reference."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_details
except ImportError:
    from streamtex import show_details


class BlockStyles:
    """Commands Reference styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Reference table of all 14 CE commands (13 here + go in its own block) with options and examples."""

    st_space("v", 1)
    st_write(bs.heading, "Commands Reference",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "Compound Document Engineering provides ", (s.bold, "14 commands"),
             " that map directly to the CE ",
             (s.project.titles.phase_kw, "phases"),
             ". Each command activates the ",
             (s.project.titles.concept_kw, "agents"),
             " for its phase, reads inputs from prior phases, and writes "
             "structured outputs.")
    st_space("v", 1)

    show_details("""
    ### Command Overview

    | Command | Phase | Purpose |
    |---------|-------|---------|
    | `/stx-ce:collect` | COLLECT | Scan sources, build inventory |
    | `/stx-ce:assess` | ASSESS | Analyze content, identify gaps or angles, initialize master plan (1st iteration) or enrich it |
    | `/stx-ce:plan` | PLAN | Design the increment plan in coherence with the master plan; 1st iteration also produces the global TOC skeleton |
    | `/stx-ce:prototype` | PROTOTYPE | Validate styles by example via pilot block(s); capture/reuse patterns into the local catalog. QCM-driven, skipped when the increment continues a validated visual territory |
    | `/stx-ce:produce` | PRODUCE | Generate or convert blocks; apply patterns mapped in the master plan |
    | `/stx-ce:review` | REVIEW | Quality check from 5 perspectives (objective-monitor consulted in sequence) |
    | `/stx-ce:fix` | FIX | Apply review recommendations; may propose re-applying new patterns to earlier blocks |
    | `/stx-ce:compound` | COMPOUND | Extract and package learnings across 4 axes (production, ecosystem feedback, dev governance, master plan maintenance) |
    | `/stx-ce:integrate` | INTEGRATE | Route solutions; promote local patterns to the shared catalog when eligible |
    | `/stx-ce:status` | (any) | Show current cycle state and master plan dashboard |
    | `/stx-ce:task` | (any) | Execute an ad-hoc task with lifecycle reconciliation |
    | `/stx-ce:pause` | (any) | Save session checkpoint before pausing work (snapshots the master plan if state changed) |
    | `/stx-ce:continue` | (any) | Resume work after a session break (runs plan-reconciler and objective-monitor) |
    """)

    st_space("v", 1)

    show_details("""
    ### /stx-ce:collect

    **Syntax**: `/stx-ce:collect [path] [--project .] [--brief "description"] [--sources dir1 dir2]`

    | Option | Description | Pathway |
    |--------|-------------|---------|
    | `path` | Directory containing source files to scan | A |
    | `--project .` | Scan current StreamTeX project | B |
    | `--brief "..."` | Provide project description (no files) | C |
    | `--sources` | Explicit list of source directories to scan | A |

    **Agents activated**: source-scanner, import-assessor (pathway A only)
    **Output**: `docs/inventory.md`
    **Required reading**: inventory report before proceeding to assess

    **Examples**:
    ```
    /stx-ce:collect ./legacy-html/
    /stx-ce:collect --project .
    /stx-ce:collect --brief "API reference for the analytics module"
    ```
    """)

    st_space("v", 1)

    show_details("""
    ### /stx-ce:assess

    **Syntax**: `/stx-ce:assess [--pathway A|B|C] [--skip-audience]`

    | Option | Description | Default |
    |--------|-------------|---------|
    | `--pathway` | Force a specific pathway | Auto-detected |
    | `--skip-audience` | Reuse audience profile from prior cycle | Off |

    **Agents activated**: audience-analyst, content-strategist,
    gap-analyst (A/B) or angle-generator (C), format-explorer
    **Requires**: completed COLLECT phase
    **Output**: `docs/assessment.md`
    **Required reading**: assessment brief, especially gap report or angle proposals

    **Examples**:
    ```
    /stx-ce:assess
    /stx-ce:assess --pathway C
    /stx-ce:assess --skip-audience
    ```
    """)

    st_space("v", 1)

    show_details("""
    ### /stx-ce:plan

    **Syntax**: `/stx-ce:plan [--interactive] [--max-blocks N] [--focus "area"]`

    | Option | Description | Default |
    |--------|-------------|---------|
    | `--interactive` | 4-step collaborative planning process | Auto mode |
    | `--max-blocks` | Limit the number of blocks planned | No limit |
    | `--focus` | Concentrate on a specific part or topic | Full scope |

    **Agents activated**: structure-planner, task-sequencer
    **Requires**: completed ASSESS phase
    **Output**: `docs/plan.md`

    **Examples**:
    ```
    /stx-ce:plan
    /stx-ce:plan --max-blocks 10 --focus "getting started"
    ```
    """)

    st_space("v", 1)

    show_details("""
    ### /stx-ce:produce, /stx-ce:review, /stx-ce:fix, /stx-ce:compound

    **`/stx-ce:produce`** `[--block NAME] [--dry-run]`
    - `--block`: produce a single specific block instead of all
    - `--dry-run`: show what would be produced without writing files
    - Agents: block-writer, style-applicator, content-migrator (pathway A)

    **`/stx-ce:review`** `[--perspective NAME] [--block NAME]`
    - `--perspective`: run only one reviewer (e.g., `visual-reviewer`)
    - `--block`: review a single block
    - Output: `docs/review.md`

    **`/stx-ce:fix`** `[--severity CRITICAL|MAJOR|MINOR] [--auto] [--thorough] [--dry-run]`
    - `--severity`: fix only findings at or above the given severity
    - `--auto`: apply fixes without confirmation prompts
    - `--thorough`: include minor and suggestion-level improvements
    - `--dry-run`: show planned fixes without applying

    **`/stx-ce:compound`** `[--skip-solutions] [--skip-profile] [--skip-feedback]`
    - Selectively skip capitalization axes
    - Agents: feedback-detector, dev-governance
    - Output: `docs/solutions/`, `docs/profile.md`, `docs/feedback/`
    """)

    st_space("v", 1)

    show_details("""
    ### /stx-ce:status

    **Syntax**: `/stx-ce:status [--verbose] [--help]`

    | Option | Description | Default |
    |--------|-------------|---------|
    | `--verbose` | Show detailed breakdown per phase and per block | Summary only |
    | `--help` | Display usage information for the status command | Off |

    **Purpose**: Shows the CE cycle dashboard for the current project. This
    is the go-to command for understanding where you are in the cycle.

    **Dashboard contents:**
    - **Phase status** — which phases are completed, in progress, or pending
    - **Production progress** — block-by-block completion in PRODUCE phase
    - **Review findings summary** — count of findings by severity level
    - **Producer profile state** — whether a profile exists and its last update date

    **Output**: displayed in the terminal (no file written).

    **Examples**:
    ```
    /stx-ce:status
    /stx-ce:status --verbose
    ```

    **Verbose output example**:
    ```
    CE Cycle Status
    ===============
    Pathway: A (Import)
    Current phase: PRODUCE (3/5 blocks done)

    Phases:
      COLLECT   : done (2026-03-20)
      ASSESS    : done (2026-03-21)
      PLAN      : done (2026-03-21)
      PRODUCE   : in progress (3/5 blocks)
      REVIEW    : pending
      FIX       : pending
      COMPOUND  : pending

    Production:
      bck_intro_welcome    : done
      bck_chapter1_overview: done
      bck_chapter1_details : done
      bck_chapter2_overview: pending
      bck_chapter2_details : pending

    Review findings: (none yet)
    Producer profile: exists (last updated 2026-03-19)
    ```
    """)

    st_space("v", 2)
    st_write(bs.sub, "/stx-ce:task", toc_lvl="+1")
    st_space("v", 1)

    show_details("""
    **Syntax**: `/stx-ce:task "<free-text description>"`

    **Options**: `--from-plan <path>`, `--help`

    **Purpose**: Execute an ad-hoc task with lifecycle reconciliation.

    **6 Archetypes** (auto-detected):
    | Archetype | Triggers | Artifact |
    |-----------|----------|----------|
    | COMPARE | "compare", "coverage", "gaps" | `docs/reviews/YYYY-MM-DD-coverage-task.md` |
    | TARGETED REVIEW | "review", "check" + scope | `docs/reviews/YYYY-MM-DD-task-review.md` |
    | TARGETED PRODUCTION | "add", "create" | New blocks + new plan version |
    | PLAN AMENDMENT | "update plan", "reorder" | New plan version with Change Log |
    | TARGETED COMPOUND | "capitalize", "extract pattern" | `docs/solutions/` |
    | SOURCE ANALYSIS | "analyze source" | `docs/collect/YYYY-MM-DD-task-analysis.md` |

    **Agents activated**: ad-hoc-reviewer (for custom review), gap-analyst (for COMPARE), learnings-researcher (for COMPOUND)

    **Gate**: No gate for read-only tasks; confirmation for write tasks. Configurable via `task_gate` in producer profile.
    """)

    st_space("v", 2)
    st_write(bs.sub, "/stx-ce:pause", toc_lvl="+1")
    st_space("v", 1)

    show_details("""
    **Syntax**: `/stx-ce:pause [--message "<text>"]`

    **Options**: `--message` (context annotation), `--help`

    **Purpose**: Save a session checkpoint before pausing work.

    **Output**: `docs/ce-checkpoint.md` (overwritten each time)

    **Checkpoint captures**:
    - **Active work items** — blocks in progress, incomplete, out-of-plan
    - **Decisions log** — design choices, scope decisions, plan deviations
    - **Pending issues** — blockers, missing assets, partial fixes
    - **Uncommitted changes** — summary of git status
    - **Context for next session** — free-text briefing

    **Workflow**: INSPECT → DETECT in-progress → CAPTURE context → WRITE

    **Agents activated**: None (inspection-only)

    **Examples**:
    ```
    /stx-ce:pause
    /stx-ce:pause --message "Stopped mid-review, visual done, 2 remaining"
    ```
    """)

    st_space("v", 2)
    st_write(bs.sub, "/stx-ce:continue", toc_lvl="+1")
    st_space("v", 1)

    show_details("""
    **Syntax**: `/stx-ce:continue [--verbose]`

    **Options**: `--verbose` (detailed drift analysis), `--help`

    **Purpose**: Resume work after a session break.

    **Output**:
    0. **Checkpoint restore** — if `docs/ce-checkpoint.md` exists, restore and archive it
    1. **Briefing** — project name, last activity, plan version, block progress
    2. **Drift detection** — source changes, manual edits, plan mismatch, stale artifacts
    3. **Proposals** — prioritized next steps with commands (checkpoint items integrated)
    4. **Dispatch** — select proposal or describe custom task

    **Priority**: CRITICAL > HIGH > MEDIUM > LOW > INFO

    **Agents activated**: None (inspection-only, delegates to other commands)
    """)

    st_space("v", 1)

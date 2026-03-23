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
    """Reference table of all 8 CE commands with options and examples."""

    st_space("v", 1)
    st_write(bs.heading, "Commands Reference",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "The Capitalization Engine provides ", (s.bold, "8 commands"),
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
    | `/stx-ce:assess` | ASSESS | Analyze content, identify gaps or angles |
    | `/stx-ce:plan` | PLAN | Design structure, sequence tasks |
    | `/stx-ce:produce` | PRODUCE | Generate or convert blocks |
    | `/stx-ce:review` | REVIEW | Quality check from 5 perspectives |
    | `/stx-ce:fix` | FIX | Apply review recommendations |
    | `/stx-ce:compound` | COMPOUND | Extract and package learnings |
    | `/stx-ce:status` | (any) | Show current cycle state and progress |
    """)

    show_details("""
    ### /stx-ce:collect

    **Syntax**: `/stx-ce:collect [path] [--project .] [--brief "description"]`

    | Option | Description | Pathway |
    |--------|-------------|---------|
    | `path` | Directory containing source files to scan | A |
    | `--project .` | Scan current StreamTeX project | B |
    | `--brief "..."` | Provide project description (no files) | C |

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

    show_details("""
    ### /stx-ce:plan

    **Syntax**: `/stx-ce:plan [--max-blocks N] [--focus "area"]`

    | Option | Description | Default |
    |--------|-------------|---------|
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

    **`/stx-ce:fix`** `[--severity blocker|major|minor] [--auto]`
    - `--severity`: fix only findings at or above the given severity
    - `--auto`: apply fixes without confirmation prompts

    **`/stx-ce:compound`** `[--skip-solutions] [--skip-profile] [--skip-feedback]`
    - Selectively skip capitalization axes
    - Agents: feedback-detector, dev-governance
    - Output: `docs/solutions/`, `docs/profile.md`, `docs/feedback/`

    **`/stx-ce:status`** — no options, shows cycle state:
    ```
    CE Cycle Status
    ===============
    Pathway: A (Import)
    Current phase: PRODUCE (3/5 blocks done)
    Inventory: 12 sources | Assessment: 8 gaps | Plan: 5 blocks
    ```
    """)

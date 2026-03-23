"""CE Manual — Part 2: /stx-ce:go Autonomous Workflow."""

from streamtex import *

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details

from custom.styles import Styles as s


class BlockStyles:
    """Styles for the /stx-ce:go block."""
    title = s.part_title if hasattr(s, "part_title") else {}
    phase = s.phase if hasattr(s, "phase") else {}


def build():
    """/stx-ce:go autonomous workflow: 11 steps, 3 gates, flags."""

    st_write("""
    ## /stx-ce:go — The Autonomous Pipeline

    The `/stx-ce:go` command runs the **complete CE cycle** as an autonomous
    pipeline. It chains all phases (COLLECT through COMPOUND) with automatic
    gate checks and configurable behavior flags.

    This is the primary command for production use. Individual phase commands
    exist for debugging and fine-tuning, but `/stx-ce:go` is the standard
    entry point.
    """)

    show_explanation("The 11-Step Pipeline", """
    ```
    /stx-ce:go
      |
      Step  1: COLLECT sources .................. scan & classify
      Step  2: COLLECT report ................... generate manifest
      |
      === GATE 1: Source validation ===
      |  Abort if: no usable sources found
      |  Pause if: >50% items are out-of-scope
      |
      Step  3: ASSESS pathway ................... detect A/B/C
      Step  4: ASSESS requirements .............. dialogue (R1-R18)
      Step  5: PLAN skeleton .................... structure
      Step  6: PLAN sequence .................... ordering & milestones
      |
      === GATE 2: Plan approval ===
      |  Pause: user must confirm plan (auto-confirm with --quick)
      |  Abort if: plan has 0 producible blocks
      |
      Step  7: PRODUCE blocks ................... create/import/improve
      Step  8: REVIEW evaluation ................ 5-agent analysis
      Step  9: FIX corrections .................. apply & verify
      |
      === GATE 3: Quality threshold ===
      |  Loop: REVIEW-FIX up to 3 times if CRITICAL findings remain
      |  Abort if: quality score < 50% after 3 iterations
      |
      Step 10: COMPOUND capitalize .............. profile + tickets
      Step 11: COMPOUND governance .............. commit + merge
      |
      DONE
    ```
    """)

    show_explanation("The 3 Gates", """
    Gates are automatic checkpoints that can pause or abort the pipeline:

    **Gate 1 — Source Validation** (after COLLECT)
    - Verifies that at least some usable sources were found
    - Warns if most items are out-of-scope (possible wrong directory)
    - In `--quick` mode: skips if pathway C is viable

    **Gate 2 — Plan Approval** (after PLAN)
    - Presents the production plan for user confirmation
    - In `--quick` mode: auto-confirms if plan looks reasonable
    - In `--interactive` mode: enters the 4-step planning process
    - Aborts if the plan contains zero producible blocks

    **Gate 3 — Quality Threshold** (after REVIEW/FIX)
    - Checks that no CRITICAL findings remain after FIX
    - Triggers REVIEW-FIX loop (max 3 iterations) if needed
    - Aborts if quality score stays below 50% after all iterations
    - In `--quick` mode: accepts WARNING-level quality
    """)

    show_explanation("Behavior Flags", """
    Flags customize how `/stx-ce:go` operates:

    | Flag | Effect |
    |------|--------|
    | `--quick` | Auto-confirm gates, skip INFO fixes, minimal dialogue |
    | `--interactive` | Full dialogue at every phase, 4-step planning |
    | `--review-only` | Stop after REVIEW (no FIX, no COMPOUND) |
    | `--import` | Pathway A forced: import-only, no creation |
    | `--improve` | Process only IMPROVE-tagged blocks |

    **Flag combinations:**
    - `--quick --import`: fastest path for bulk import jobs
    - `--interactive --review-only`: careful review without auto-fix
    - `--improve`: update existing project without adding new blocks

    **Default behavior** (no flags): balanced mode with gate pauses,
    auto pathway detection, REVIEW-FIX loop enabled.
    """)

    show_details("Full Pipeline Diagram", """
    ```
    [COLLECT] -> [ASSESS] -> [PLAN] -> [PRODUCE] -> [REVIEW] -> [FIX] -> [COMPOUND]
        |            |          |           |            |          |          |
      scan       pathway     skeleton    execute     5 agents    apply    capitalize
      classify   dialogue    sequence    per-type    severity    verify   feedback
      report     R1-R18      milestones  validate    report      loop     governance
        |            |          |           |            |          |          |
      Gate 1       auto/     Gate 2      resume      read-     Gate 3    commit
      validate   interactive  approve    on fail     only       quality   merge
    ```
    """)

    show_details("Command Reference", """
    ```bash
    # Full autonomous pipeline (default)
    /stx-ce:go

    # Quick mode (minimal interaction)
    /stx-ce:go --quick

    # Interactive mode (full control)
    /stx-ce:go --interactive

    # Import-only pipeline
    /stx-ce:go --import --sources ./slides ./docs

    # Review existing project without changes
    /stx-ce:go --review-only

    # Improve existing blocks only
    /stx-ce:go --improve

    # Resume after interruption
    /stx-ce:go --resume

    # Dry run (show pipeline steps without executing)
    /stx-ce:go --dry-run
    ```

    Pipeline state is persisted in `.ce/pipeline-state.json` for resumability.
    """)

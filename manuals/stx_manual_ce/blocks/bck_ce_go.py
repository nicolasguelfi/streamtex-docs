"""CE Manual — Part 2: /stx-ce:go Autonomous Workflow."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """/stx-ce:go styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """/stx-ce:go autonomous workflow: 11 steps, 3 gates, flags."""

    st_space("v", 1)
    st_write(bs.heading, "/stx-ce:go — The Autonomous Pipeline",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "The ",
             (s.project.titles.tool_kw, "/stx-ce:go"),
             " command runs the ",
             (s.bold, "complete CE cycle"),
             " as an autonomous pipeline. It chains all phases (",
             (s.project.titles.phase_kw, "COLLECT"),
             " through ",
             (s.project.titles.phase_kw, "COMPOUND"),
             ") with automatic gate checks and configurable behavior flags.")
    st_space("v", 1)

    st_write(s.large,
             "This is the primary command for production use. Individual phase commands "
             "exist for debugging and fine-tuning, but ",
             (s.project.titles.tool_kw, "/stx-ce:go"),
             " is the standard entry point.")
    st_space("v", 1)

    show_explanation("""\
    ### The 11-Step Pipeline

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

    st_space("v", 1)

    show_explanation("""\
    ### The 3 Gates

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

    st_space("v", 1)

    show_explanation("""\
    ### Behavior Flags

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

    st_space("v", 1)

    show_details("""\
    ### Full Pipeline Diagram

    ```
    [COLLECT] -> [ASSESS] -> [PLAN] -> [PROTOTYPE] -> [PRODUCE] -> [REVIEW] -> [FIX] -> [COMPOUND] -> [INTEGRATE]
        |            |          |           |            |             |          |          |             |
      scan       pathway     skeleton    pilot         execute     5 agents    apply    capitalize    route +
      classify   dialogue    +           block(s),     per-type    parallel    fixes    4 axes        promote
      report     R1-R18,     master      patterns     +            +           +        +              patterns
                 master      plan        captured     patterns     objective   re-      master         to shared
                 plan init               or reused    applied      monitor     apply    plan upkeep    catalog
        |            |          |           |            |             |          |          |             |
                              Gate 1     (QCM-driven, skipped if no                 Gate 2     Gate 3      Gate 4
                              approve    new visual territory)                      lance fix  next       integrate
    ```

    Gates 1-4 are the four **fundamental** QCM checkpoints (post-PLAN, post-REVIEW, post-FIX, post-INTEGRATE). PROTOTYPE is QCM-driven and may be skipped when the increment continues an already-validated visual territory.
    """)

    st_space("v", 1)

    show_details("""\
    ### Command Reference

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

    Pipeline state is persisted in `docs/pipeline-state.json` for resumability.
    """)

    st_space("v", 2)
    st_write(bs.sub, "Which command should I use?", toc_lvl="+1")
    st_space("v", 1)

    show_details("""
    ### Choosing the right CE command

    | Situation | Command | Why |
    |-----------|---------|-----|
    | Start a new project or full production cycle | `/stx-ce:go` | Runs all 9 phases with 4 fundamental gates (PROTOTYPE is QCM-driven) |
    | Do a specific punctual task (compare, review, add block) | `/stx-ce:task "..."` | Targeted execution with lifecycle reconciliation |
    | Return after a break, unsure where you left off | `/stx-ce:continue` | Briefing + drift detection + proposals |
    | Run a specific phase directly | `/stx-ce:collect`, `:review`, etc. | Direct control, no orchestration |
    | Check project status without action | `/stx-ce:status` | Read-only diagnostic |
    """)

    st_space("v", 1)

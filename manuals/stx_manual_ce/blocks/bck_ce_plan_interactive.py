"""CE Manual — Part 2: Interactive Planning."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """Interactive Planning styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Interactive planning: the 4-step skeleton-first approach."""

    st_space("v", 1)
    st_write(bs.heading, "Interactive Planning — The Skeleton-First Approach",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "When ",
             (s.project.titles.tool_kw, "/stx-ce:plan --interactive"),
             " is used, the CE engine walks through a ",
             (s.bold, "4-step collaborative process"),
             ". Each step builds on the previous one, "
             "and the user has full control at every decision point.")
    st_space("v", 1)

    st_write(s.large,
             "The key principle: ",
             (s.bold, "skeleton first, details later"),
             ". Structure drives everything else.")
    st_space("v", 1)

    show_explanation("Step 1: Skeleton", """
    The first and most important step defines the structural backbone.

    **What happens:**
    1. CE proposes an initial skeleton based on the assess report
    2. The user reviews and modifies: add/remove/reorder parts and blocks
    3. Each block gets a type tag: `[IMPORT]`, `[IMPROVE]`, or `[CREATE]`
    4. The skeleton is locked when the user confirms

    **User interaction:**
    ```
    CE: Here is the proposed skeleton for "my-course":

        Part 1: Getting Started (3 blocks)
          bck_start_welcome    [CREATE]
          bck_start_install    [IMPORT] <- from slides/setup.pptx
          bck_start_first_run  [CREATE]

        Part 2: Core Concepts (4 blocks)
          ...

    > Modify? (add/remove/reorder/rename/confirm)
    ```

    The skeleton determines the total scope. Everything downstream
    respects this structure.
    """)

    st_space("v", 1)

    show_explanation("Step 2: Objectives", """
    With the skeleton locked, CE assigns learning objectives to each block.

    **What happens:**
    1. CE proposes per-block micro-objectives based on block names and types
    2. Per-part summary objectives are generated
    3. The user validates, refines, or adds objectives
    4. Objectives are linked to assessment criteria (optional)

    **Example:**
    ```
    Part 1: Getting Started
      Objective: "Reader can install and run the project"

      bck_start_welcome:
        -> "Reader understands the purpose and scope"
      bck_start_install:
        -> "Reader has a working local environment"
      bck_start_first_run:
        -> "Reader has executed the first example successfully"
    ```
    """)

    st_space("v", 1)

    show_explanation("Step 3: Design", """
    Design decisions are made block by block, with sensible defaults.

    **What happens:**
    1. CE proposes a style profile (or uses the project default)
    2. For each block, CE suggests interaction patterns:
       - Expanders for optional details
       - Tabs for alternative approaches
       - Columns for side-by-side comparison
       - Code blocks with copy buttons
    3. The user accepts defaults or customizes per block

    **Design tokens:**
    ```
    bck_start_welcome:  [hero-banner, expander:prerequisites]
    bck_start_install:  [tabs:os-specific, code:copy]
    bck_start_first_run: [columns:code|output, expander:troubleshoot]
    ```
    """)

    st_space("v", 1)

    show_explanation("Step 4: Final Plan", """
    The final step assembles everything into the production plan.

    **What happens:**
    1. CE computes the production sequence (dependency order)
    2. Milestones are placed at natural breakpoints
    3. Effort estimates are calculated per block
    4. The complete plan is presented for final approval

    **The user can:**
    - Approve the plan and proceed to PRODUCE
    - Go back to any previous step to make changes
    - Save the plan as a template for future projects
    - Export the plan as a standalone document

    Once approved, the plan is **immutable** during PRODUCE. Changes require
    re-entering PLAN with `/stx-ce:plan --revise`.
    """)

    st_space("v", 1)

    show_details("Command Reference", """
    ```bash
    # Start interactive planning
    /stx-ce:plan --interactive

    # Resume from a specific step
    /stx-ce:plan --interactive --from-step 2

    # Save plan as reusable template
    /stx-ce:plan --interactive --save-template my-course-template

    # Load a previously saved plan template
    /stx-ce:plan --from-template my-course-template
    ```

    Interactive plans are saved incrementally. If interrupted, the process
    resumes from the last completed step.
    """)

    st_space("v", 1)

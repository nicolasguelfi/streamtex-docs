"""CE Manual — Part 2: PLAN Phase."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """PLAN phase styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """PLAN phase: auto mode vs interactive mode."""

    st_space("v", 1)
    st_write(bs.heading, "PLAN — Structure the Production Plan",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "The ",
             (s.project.titles.phase_kw, "PLAN"),
             " phase transforms the assessment results into a concrete, "
             "actionable production plan. It defines the project skeleton, learning "
             "objectives, design choices, and production sequence.")
    st_space("v", 1)

    st_write(s.large,
             (s.project.titles.phase_kw, "PLAN"),
             " operates in two modes: ",
             (s.bold, "auto"),
             " (for experienced users) and ",
             (s.bold, "interactive"),
             " (for fine-grained control).")
    st_space("v", 1)

    show_explanation("""\
    ### The Plan Structure

    Every CE plan contains four components, produced in order:

    **1. SKELETON** — The structural backbone
    - Parts, chapters, sections hierarchy
    - Block inventory with types and names
    - Navigation flow and cross-references

    **2. OBJECTIVES** — What each section achieves
    - Per-part learning goals
    - Per-block micro-objectives
    - Assessment criteria (if applicable)

    **3. DESIGN** — Visual and interaction choices
    - Style profile selection or customization
    - Widget and interaction patterns
    - Layout decisions (columns, tabs, expanders)

    **4. SEQUENCE** — The production order
    - Which blocks to produce first (dependencies)
    - Parallelizable work items
    - Milestone checkpoints
    """)

    st_space("v", 1)

    show_explanation("""\
    ### Auto Mode vs Interactive Mode

    | Aspect | Auto Mode | Interactive Mode |
    |--------|-----------|------------------|
    | **Speed** | Fast (minutes) | Deliberate (iterative) |
    | **User input** | Confirm/reject only | Step-by-step decisions |
    | **Best for** | Standard projects | Complex or custom projects |
    | **Skeleton** | Generated from templates | Built collaboratively |
    | **Objectives** | Inferred from content | Explicitly defined |
    | **Design** | Default profile applied | Custom choices at each step |
    | **Sequence** | Dependency-sorted | User-prioritized |

    **Auto mode** generates the complete plan in one pass and presents it
    for approval. The user can accept, modify, or reject.

    **Interactive mode** walks through each of the 4 components step by step,
    asking for user input at each decision point. See the next block for
    details on the interactive 4-step approach.
    """)

    st_space("v", 1)

    show_explanation("""\
    ### Plan Output Format

    The plan is saved as a structured document with executable metadata:

    ```
    === CE PRODUCTION PLAN ===
    Project: my-training-course
    Pathway: B (Balanced)
    Mode: auto
    Total blocks: 24
    Estimated effort: 12 PRODUCE cycles

    SKELETON:
      Part 1: Introduction (4 blocks)
        bck_intro_welcome    [CREATE]  priority: 1
        bck_intro_overview   [IMPORT]  priority: 1
        bck_intro_setup      [IMPROVE] priority: 2
        bck_intro_first_step [CREATE]  priority: 2
      Part 2: Core Concepts (6 blocks)
        ...

    SEQUENCE:
      Milestone 1: Part 1 complete (4 blocks)
      Milestone 2: Parts 2-3 complete (14 blocks)
      Milestone 3: Full project (24 blocks)
    ```
    """)

    st_space("v", 1)

    show_details("""\
    ### Command Reference

    ```bash
    # Auto-plan from assess report
    /stx-ce:plan

    # Interactive planning (4-step approach)
    /stx-ce:plan --interactive

    # Re-plan with modified skeleton
    /stx-ce:plan --revise skeleton

    # Plan for specific parts only
    /stx-ce:plan --parts 1,2,3
    ```

    The plan is saved to `docs/plan.md` and drives the PRODUCE phase.
    """)

    st_space("v", 1)

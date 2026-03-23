"""CE Manual — Part 4: Guide — Improve a StreamTeX Project (Pathway B)."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """Improve Guide styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Guide: Improve a StreamTeX project — Pathway B walkthrough."""

    st_space("v", 1)
    st_write(bs.heading, "Guide: Improve a StreamTeX Project (Pathway B)",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             (s.project.titles.pathway_kw, "Pathway B"),
             (" is for projects that already exist as StreamTeX but need "
              "enhancement: adding new sections, fixing quality issues, updating "
              "outdated content, or restructuring for better flow. Unlike "),
             (s.project.titles.pathway_kw, "Pathway A"),
             (", there is no format conversion — the work is purely about content "
              "and structure improvement."))
    st_space("v", 1)

    show_explanation("""
    ### Step 1: COLLECT — Inventory Current State

    ```
    /stx-ce:collect --project .
    ```

    When pointed at an existing StreamTeX project, the **source-scanner**
    operates in project mode:

    - Scans all blocks in `blocks/` — counts lines, identifies components used
    - Reads `book.py` for structure: parts, block order, navigation
    - Catalogs custom styles, helpers, and assets
    - Notes the last modification date of each block
    - Records any existing `docs/` artifacts from prior CE cycles

    The **import-assessor** is skipped in Pathway B since there is no
    external material to convert.

    **Output**: a project inventory in `docs/inventory.md` showing the
    full current state of the project.
    """)

    show_explanation("""
    ### Step 2: ASSESS — Identify Gaps and Opportunities

    ```
    /stx-ce:assess
    ```

    The agents evaluate the project against your improvement goals:

    - **audience-analyst** re-evaluates whether the content still matches
      the target audience (audiences evolve over time).
    - **content-strategist** checks theme coverage and learning objectives
      against current needs.
    - **gap-analyst** performs a thorough comparison:
      - Missing topics that should be covered
      - Outdated content that needs refreshing
      - Structural weaknesses (e.g., blocks that are too long, parts
        that lack coherence)
      - Style inconsistencies accumulated over time

    The gap report is the key output here. It drives all subsequent work.
    """)

    show_details("""
    ### Common Gap Categories in Pathway B

    | Category | Example | Typical Severity |
    |----------|---------|------------------|
    | content-missing | No block covering the new API v2 features | critical |
    | content-outdated | Examples use deprecated function names | major |
    | structure-imbalance | Part 3 has 12 blocks, Part 4 has only 2 | major |
    | style-drift | Early blocks use old naming conventions | minor |
    | flow-break | No transition between theory and practice sections | major |
    | redundancy | Same concept explained in two different blocks | minor |
    | depth-mismatch | Advanced topic explained too superficially | important |
    """)

    show_explanation("""
    ### Step 3: PLAN — Prioritize Improvements

    ```
    /stx-ce:plan
    ```

    The **structure-planner** designs the improved structure:
    - Where new blocks fit in the existing skeleton
    - Which blocks need splitting, merging, or reordering
    - Updated navigation flow

    The **task-sequencer** creates a prioritized task list:
    - Critical gaps first, then major, then minor
    - Respects dependencies (update a shared helper before blocks that use it)
    - Groups related changes to minimize context switching

    **Important**: the plan should be conservative. Resist the urge to rewrite
    everything — focus on the gaps identified in the assessment.
    """)

    show_explanation("""
    ### Step 4: PRODUCE — Implement Improvements

    ```
    /stx-ce:produce
    ```

    The **block-writer** and **style-applicator** handle production:

    - **New blocks**: written from scratch following plan specifications
    - **Updated blocks**: modified in place, preserving working content
    - **Restructured blocks**: split or merged as planned, with content
      redistributed appropriately
    - **Style fixes**: conventions updated across affected blocks

    Pathway B production is often faster than Pathway A because the
    project infrastructure (book.py, styles, helpers) already exists.
    The work is incremental rather than foundational.
    """)

    show_details("""
    ### Steps 5-6: REVIEW, FIX, and COMPOUND

    **Review** focuses on improvement-specific concerns:
    ```
    /stx-ce:review
    ```

    Reviewers pay special attention to:
    - **Integration**: do new blocks blend with existing ones?
    - **Regression**: did changes break anything that was working?
    - **Consistency**: are updated blocks consistent with untouched ones?

    **Fix** and **Compound** work identically to Pathway A:
    ```
    /stx-ce:fix
    /stx-ce:compound
    ```

    The COMPOUND phase is especially valuable in Pathway B because
    improvement cycles often reveal reusable patterns:
    - "Every project needs a glossary block" becomes a solution template
    - "Always check for deprecated API usage" becomes a profile convention
    - "The gap-analyst misses style drift" becomes ecosystem feedback

    **Pathway B can be iterative** — run multiple B cycles on the same
    project, each time tackling a different set of improvements. The
    producer profile accumulates knowledge across cycles.
    """)

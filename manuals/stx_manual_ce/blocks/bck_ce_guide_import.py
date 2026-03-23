"""CE Manual — Part 4: Guide — Import Existing Material (Pathway A)."""

from streamtex import *

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details

from custom.styles import Styles as s


class BlockStyles:
    """Styles for the import guide block."""

    title = s.section_title
    table = s.reference_table


def build():
    """Guide: Import existing material — Pathway A walkthrough."""

    st_write("""
    ## Guide: Import Existing Material (Pathway A)

    This guide walks through the complete CE cycle for the most common
    scenario: you have existing documents (HTML pages, Marp presentations,
    PDFs) and want to convert them into a StreamTeX project. Pathway A
    is designed for exactly this situation.
    """)

    show_explanation("""
    ### Step 1: COLLECT — Gather Your Sources

    Start by organizing your source files in a working directory. Then
    run the collection phase:

    ```
    /stx-ce:collect path/to/sources/
    ```

    The **source-scanner** agent will:
    - Recursively detect all supported files (HTML, MD, Marp, PDF, images)
    - Extract metadata: word counts, headings, images, tables
    - Map dependencies between files (shared images, stylesheets)
    - Produce a source inventory saved to `docs/inventory.md`

    The **import-assessor** then evaluates each source:
    - Assigns complexity scores (low / medium / high)
    - Recommends conversion method (automated / assisted / manual)
    - Estimates effort for each source
    - Ranks sources by import priority

    **Review the inventory** before proceeding. Remove sources you do not
    want to import, and adjust priorities if needed.
    """)

    show_explanation("""
    ### Step 2: ASSESS — Analyze Content and Gaps

    ```
    /stx-ce:assess
    ```

    Three agents activate in sequence:
    - **audience-analyst** profiles your target readers
    - **content-strategist** maps themes and learning objectives
    - **gap-analyst** compares source content against the target structure

    The output is an **assessment brief** in `docs/assessment.md` containing:
    - Audience profile and tone recommendations
    - Content map with theme relationships
    - Gap report listing missing, redundant, and restructuring needs

    **Key decision point**: the gap report may reveal that some source content
    is outdated or irrelevant. Mark those items as "skip" before planning.
    """)

    show_explanation("""
    ### Step 3: PLAN — Design the Structure

    ```
    /stx-ce:plan
    ```

    The **structure-planner** designs the document skeleton:
    - Parts, blocks, and navigation flow
    - Mapping from source sections to target blocks

    The **task-sequencer** orders the production work:
    - Which blocks to produce first (respecting dependencies)
    - Estimated time per block
    - Parallelization opportunities

    Review the plan in `docs/plan.md`. Adjust block names, reorder parts,
    or split/merge blocks as needed.
    """)

    show_details("""
    ### Step 4: PRODUCE — Convert Content

    ```
    /stx-ce:produce
    ```

    This is where the actual conversion happens. Three agents collaborate:

    - **content-migrator** handles the format conversion:
      - HTML sources: `/stx-import:html` automated conversion
      - Marp sources: `/stx-import:marp` slide-to-block mapping
      - PDF sources: text extraction + manual block writing
    - **block-writer** generates new blocks for gap-filling content
    - **style-applicator** applies your `custom/styles.py` consistently

    **Production order follows the task-sequencer's plan.** Each block is
    written, saved, and checked for basic syntax before moving to the next.

    | Source Type | Method | Agent |
    |-------------|--------|-------|
    | HTML (low complexity) | Automated `/stx-import:html` | content-migrator |
    | HTML (medium) | Assisted conversion + fixup | content-migrator + block-writer |
    | Marp (any) | `/stx-import:marp` + restructure | content-migrator |
    | PDF | Manual rewrite from reference | block-writer |
    | Gap content | Written from scratch | block-writer |
    """)

    show_explanation("""
    ### Step 5: REVIEW — Quality Check

    ```
    /stx-ce:review
    ```

    All five review perspectives examine the produced blocks:
    1. **audience-advocate**: Is the content clear for the target audience?
    2. **pedagogy-analyst**: Does the learning flow work?
    3. **visual-reviewer**: Is the layout clean and balanced?
    4. **style-consistency-checker**: Are conventions followed?
    5. **content-editor**: Is the text accurate and well-written?

    Review findings are saved to `docs/review.md`. Each finding has a
    severity (blocker / major / minor / suggestion) and a specific fix
    recommendation.
    """)

    show_details("""
    ### Step 6: FIX and COMPOUND

    **Fix** blockers and major issues:
    ```
    /stx-ce:fix
    ```

    This re-runs affected agents on the flagged blocks only, applying
    the review recommendations. You can also fix manually and re-run
    `/stx-ce:review` to verify.

    **Compound** the cycle's learnings:
    ```
    /stx-ce:compound
    ```

    The feedback-detector and dev-governance agents:
    - Package reusable conversion patterns as solutions
    - Update your producer profile with import skills gained
    - Draft ecosystem feedback if tool issues were encountered

    **Typical Pathway A timeline:**
    | Phase | Duration (small project) | Duration (large project) |
    |-------|--------------------------|--------------------------|
    | COLLECT | 5-10 minutes | 15-30 minutes |
    | ASSESS | 10-15 minutes | 30-60 minutes |
    | PLAN | 10-15 minutes | 20-40 minutes |
    | PRODUCE | 30-60 minutes | 2-6 hours |
    | REVIEW + FIX | 15-30 minutes | 1-2 hours |
    | COMPOUND | 5-10 minutes | 10-20 minutes |
    """)

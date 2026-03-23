"""CE Manual — Part 2: PRODUCE Phase."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """PRODUCE phase styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """PRODUCE phase: orchestration of stx-designer and stx-import."""

    st_space("v", 1)
    st_write(bs.heading, "PRODUCE — Execute the Production Plan",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "The ",
             (s.project.titles.phase_kw, "PRODUCE"),
             " phase is where blocks are actually created, imported, or "
             "improved. It orchestrates the ",
             (s.project.titles.tool_kw, "stx-designer"),
             " and ",
             (s.project.titles.tool_kw, "stx-import"),
             " command families to process each item in the plan according to its type tag.")
    st_space("v", 1)

    st_write(s.large,
             (s.project.titles.phase_kw, "PRODUCE"),
             " follows the sequence defined in ",
             (s.project.titles.phase_kw, "PLAN"),
             ", respecting dependencies and milestone checkpoints.")
    st_space("v", 1)

    show_explanation("Processing by Item Type", """
    Each block in the plan has a type tag that determines how it is processed:

    **IMPORT** — Bring existing content into StreamTeX
    1. Source file is read and parsed by the import pipeline
    2. Content is mapped to StreamTeX primitives (`st_write`, `st_code`, etc.)
    3. A new block file is generated with proper structure
    4. The block is validated against StreamTeX patterns
    - Uses: `/stx-import:convert`, `/stx-import:html`

    **IMPROVE** — Enhance existing StreamTeX blocks
    1. The existing block is loaded and analyzed
    2. Improvements are applied: better explanations, updated examples,
       richer interactions (tabs, expanders, columns)
    3. The improved block replaces the original
    4. Diff is generated for traceability
    - Uses: `/stx-designer:update`, `/stx-designer:audit`

    **CREATE** — Build new blocks from scratch
    1. Block specification is read from the plan (objectives, design tokens)
    2. Content is authored following the style profile
    3. StreamTeX patterns are applied (show_explanation, show_details, etc.)
    4. The block is written and validated
    - Uses: `/stx-designer:init`, `/stx-designer:update`
    """)

    st_space("v", 1)

    show_explanation("Orchestration Flow", """
    PRODUCE processes blocks in dependency order:

    ```
    for each milestone in plan.milestones:
        for each block in milestone.blocks:
            match block.type:
                IMPORT  -> run_import_pipeline(block)
                IMPROVE -> run_improve_pipeline(block)
                CREATE  -> run_create_pipeline(block)

            validate_block(block)
            update_progress_report()

        gate_check(milestone)  # pause if errors detected
    ```

    **Key behaviors:**
    - Blocks within the same milestone can be processed in parallel
    - A failed block does not stop the pipeline (marked for retry)
    - Progress is saved after each block (resumable on interruption)
    - Each completed milestone triggers a gate check
    """)

    st_space("v", 1)

    show_explanation("Quality Gates During Production", """
    After each milestone, PRODUCE runs a lightweight quality check:

    | Check | What it verifies |
    |-------|-----------------|
    | **Syntax** | Block file is valid Python, imports work |
    | **Structure** | `BlockStyles` class and `build()` function present |
    | **Render** | Block renders without Streamlit errors |
    | **Style** | Ruff passes with project configuration |
    | **Coherence** | Cross-references between blocks are valid |

    If critical errors are found, PRODUCE pauses and reports. The user can
    fix manually or let the FIX phase handle it later.
    """)

    st_space("v", 1)

    show_details("Command Reference", """
    ```bash
    # Execute the full production plan
    /stx-ce:produce

    # Produce a specific milestone only
    /stx-ce:produce --milestone 1

    # Produce a single block
    /stx-ce:produce --block bck_start_welcome

    # Resume after interruption
    /stx-ce:produce --resume

    # Dry run (show what would be produced)
    /stx-ce:produce --dry-run
    ```

    Production progress is tracked in `docs/produce-progress.json`.
    Block files are written to the project's `blocks/` directory.
    """)

    st_space("v", 1)

"""CE Manual — Part 2: COMPOUND Phase."""

from streamtex import *

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details

from custom.styles import Styles as s


class BlockStyles:
    """Styles for the COMPOUND phase block."""
    title = s.part_title if hasattr(s, "part_title") else {}
    phase = s.phase if hasattr(s, "phase") else {}


def build():
    """COMPOUND phase: capitalization, ecosystem feedback, governance."""

    st_write("""
    ## COMPOUND — Capitalize and Feed the Ecosystem

    The **COMPOUND** phase closes the CE cycle by extracting value from the
    production process itself. It operates along three axes: production
    capitalization, ecosystem feedback, and development governance.

    COMPOUND ensures that every CE cycle makes the next one faster and
    better.
    """)

    show_explanation("Axis 1: Production Capitalization", """
    The **producer profile** captures reusable knowledge from the cycle.

    **What is capitalized:**
    - Block templates that worked well (extracted as reusable patterns)
    - Style decisions that proved effective
    - Content structures that matched the audience
    - Import mappings (source format to StreamTeX patterns)

    **The Producer Profile:**
    ```
    producer-profile.toml:
      [preferences]
      heading_style = "sentence-case"
      code_pattern = "tabs-by-language"
      explanation_depth = "intermediate"

      [templates]
      intro_block = "bck_template_intro_v2"
      concept_block = "bck_template_concept_v3"

      [import_mappings]
      pptx_slide = "one-block-per-slide"
      html_section = "preserve-hierarchy"
    ```

    The profile grows across cycles. After 3-5 projects, production speed
    increases measurably because the CE engine reuses proven patterns.
    """)

    show_explanation("Axis 2: Ecosystem Feedback", """
    Issues discovered during production are fed back to the StreamTeX
    ecosystem via `/stx-issue:*` ticket submission.

    **Ticket types:**

    | Type | Example | Target |
    |------|---------|--------|
    | **Bug** | Import pipeline fails on nested tables | streamtex library |
    | **Feature** | Need `st_accordion` widget | streamtex library |
    | **Doc** | Missing example for `st_tabs` nesting | streamtex-docs |
    | **Profile** | Style rule conflict in presentation mode | streamtex-claude |

    **Automatic detection:**
    - Import failures generate bug tickets automatically
    - Missing API coverage is detected during PRODUCE
    - Style conflicts found during REVIEW become profile tickets

    Tickets include full reproduction context (block file, error trace,
    environment info) so they can be acted on without back-and-forth.
    """)

    show_explanation("Axis 3: Dev Governance", """
    COMPOUND manages the development branch lifecycle for the project.

    **Branch management:**
    ```
    main  ----+-----------------------------+---> (stable)
              |                             |
              +-- ce/cycle-001 --+-- merge -+
                                 |
              COLLECT -> ... -> COMPOUND
    ```

    **What COMPOUND does:**
    1. Commits all produced and fixed blocks with structured messages
    2. Generates a cycle summary (blocks created, imported, improved)
    3. Creates a pull request (or merges directly if `--auto-merge`)
    4. Tags the release with cycle metadata
    5. Cleans up working files (`.ce/` reports, temp files)

    **Commit message format:**
    ```
    ce(cycle-001): PRODUCE bck_intro_welcome [CREATE]
    ce(cycle-001): FIX bck_start_install [CRITICAL] add BlockStyles
    ce(cycle-001): COMPOUND cycle complete (24 blocks, 3 iterations)
    ```
    """)

    show_details("Command Reference", """
    ```bash
    # Run full COMPOUND phase
    /stx-ce:compound

    # Capitalize only (no git operations)
    /stx-ce:compound --capitalize-only

    # Submit ecosystem tickets only
    /stx-ce:compound --feedback-only

    # Auto-merge to main
    /stx-ce:compound --auto-merge

    # Skip cleanup (keep .ce/ reports)
    /stx-ce:compound --keep-reports
    ```

    COMPOUND marks the end of the CE cycle. The project is ready for
    deployment or the next cycle iteration.
    """)

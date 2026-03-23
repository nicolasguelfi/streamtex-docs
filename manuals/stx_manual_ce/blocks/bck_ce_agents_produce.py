"""CE Manual — Part 3: PRODUCE Agents Detail."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """PRODUCE Phase Agents styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """PRODUCE phase: 4-phase orchestration with 3 production pipelines."""

    st_space("v", 1)
    st_write(bs.heading, "PRODUCE Phase Agents",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             ("The ", (s.project.titles.phase_kw, "PRODUCE"),
              " phase executes the approved plan by orchestrating ",
              (s.project.titles.tool_kw, "/stx-designer"),
              " and ",
              (s.project.titles.tool_kw, "/stx-import"),
              " commands across four phases. Each plan item is routed through "
              "one of three pipelines based on its type: ",
              (s.project.titles.pathway_kw, "Import"),
              ", ",
              (s.project.titles.pathway_kw, "Improve"),
              ", or ",
              (s.project.titles.pathway_kw, "Create"),
              ". Every item passes through an audit-fix cycle before "
              "being marked complete."))
    st_space("v", 1)

    show_explanation("""
    ### Phase 1: Initialize

    The initialization phase prepares the workspace for production.

    - **Load plan** — reads the approved structure plan from `docs/plans/`.
    - **Initialize project** — runs `/stx-designer:init` if the StreamTeX
      project does not yet exist (common for Pathway A and C).
    - **Create task list** — converts plan items into an ordered task list
      with dependencies, types (IMPORT / IMPROVE / CREATE), and status
      tracking.

    After initialization, each task is dispatched to the appropriate
    production pipeline.
    """)

    st_space("v", 1)

    show_explanation("""
    ### Phase 2: Produce Iteratively

    Each plan item is routed to one of three pipelines based on its type.
    Items are processed in the order defined by the plan, respecting
    dependencies between blocks.

    **IMPORT pipeline** (for items sourced from external files):

    1. `/stx-import:html` or `/stx-import:marp` — automated conversion
    2. `/stx-designer:audit` — quality check on the imported block
    3. `/stx-designer:fix` — correct issues found by the audit

    **IMPROVE pipeline** (for existing blocks that need enhancement):

    1. `/stx-designer:update` — apply content changes
    2. `/stx-designer:style-refactor` — align styles with `custom/styles.py`
    3. `/stx-designer:audit` — quality check
    4. `/stx-designer:fix` — correct issues

    **CREATE pipeline** (for new blocks written from scratch):

    1. `/stx-designer:block-new` or `/stx-designer:slide-new` — scaffold
    2. Write content using `stx.*` functions
    3. Apply styles from `custom/styles.py`
    4. `/stx-designer:audit` — quality check
    5. `/stx-designer:fix` — correct issues
    """)

    show_details("""
    ### Pipeline Routing Decision

    | Plan Item Type | Source | Pipeline | Primary Tool |
    |---------------|--------|----------|-------------|
    | IMPORT | HTML file | Import | `/stx-import:html` |
    | IMPORT | Marp/Markdown | Import | `/stx-import:marp` |
    | IMPROVE | Existing block | Improve | `/stx-designer:update` |
    | CREATE | New content | Create | `/stx-designer:block-new` |
    | CREATE | New slides | Create | `/stx-designer:slide-new` |

    Each pipeline ends with the same audit-fix cycle, ensuring consistent
    quality regardless of the production method.
    """)

    st_space("v", 1)

    show_explanation("""
    ### Phase 3: Global Verification

    After all individual items are produced, a global verification pass
    ensures the document works as a whole.

    - **Full audit** — `/stx-designer:audit --all` checks every block for
      style consistency, coding standards, and content completeness.
    - **Navigation check** — verifies that `book.py` references all blocks
      in the correct order and that the navigation flow matches the plan.
    - **Preview check** — runs the application to confirm visual rendering,
      responsive behavior, and absence of runtime errors.
    - **Critical fix** — any issues rated critical are fixed immediately;
      non-critical issues are logged for the REVIEW phase.
    """)

    st_space("v", 1)

    show_explanation("""
    ### Phase 4: Deliver

    The delivery phase finalizes the production cycle.

    - **Export** — runs `/stx-export:html` if the plan requires an HTML
      export artifact.
    - **Mark plan as DONE** — updates the plan status in `docs/plans/` to
      reflect completion.
    - **Production summary** — generates a report listing: items produced,
      pipelines used, issues found and fixed, and any deferred items.

    The production summary feeds into the REVIEW phase as context for the
    review agents.
    """)

    show_details("""
    ### PRODUCE Agents and Tools Summary

    The PRODUCE phase does not use standalone AI agents in the same way as
    COLLECT or ASSESS. Instead, it orchestrates existing stx-designer and
    stx-import commands, each of which encapsulates agent-like behavior:

    | Role | Tool / Command | Equivalent Agent |
    |------|---------------|-----------------|
    | Block creation | `/stx-designer:block-new`, `/stx-designer:slide-new` | block-writer |
    | Content migration | `/stx-import:html`, `/stx-import:marp` | content-migrator |
    | Style alignment | `/stx-designer:style-refactor` | style-applicator |
    | Quality check | `/stx-designer:audit` | quality-auditor |
    | Issue correction | `/stx-designer:fix` | issue-fixer |
    | Content update | `/stx-designer:update` | content-editor |

    This command-based architecture means the PRODUCE phase is fully
    traceable: every action maps to a specific command invocation that
    can be replayed or inspected.
    """)

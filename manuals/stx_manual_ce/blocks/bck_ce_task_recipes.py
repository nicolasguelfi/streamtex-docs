"""CE Manual — Part 4: Task Recipes — Real-World Patterns."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_code
except ImportError:
    from streamtex import show_explanation, show_code


class BlockStyles:
    """Task Recipes styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Six real-world task recipes for common CE ad-hoc operations."""

    st_space("v", 1)
    st_write(bs.heading, "Task Recipes",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "This section presents ",
             (s.bold, "six ready-to-use recipes"),
             " for the most common ",
             (s.project.titles.tool_kw, "/stx-ce:task"),
             " scenarios. Each recipe includes the command, a walkthrough "
             "of what happens, and the expected result.")
    st_space("v", 1)

    # ── Recipe 1: Source Coverage Audit ────────────────────────────
    st_write(bs.sub, "Source Coverage Audit", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             "You have finished producing blocks and want to verify that "
             "all source material has been covered. No content should have "
             "been silently dropped during production.")
    st_space("v", 0.5)

    show_code("""\
        /stx-ce:task coverage "Compare all collected sources with produced blocks"
    """, language="bash", line_numbers=False)
    st_space("v", 0.5)

    show_explanation("""\
    **What happens:**
    1. The gap analyst reads the source inventory from `docs/collect/`
    2. It scans all block files in `blocks/`
    3. It builds a bidirectional coverage matrix (source->blocks, blocks->source)
    4. The matrix is saved to `docs/collect/coverage-matrix.md`

    **Expected result:** A table showing each source item with its status
    (COVERED, PARTIAL, MISSING, SKIPPED) and the corresponding block(s).
    If coverage is below 70%, the gate triggers and asks you to confirm
    whether the gaps are intentional.
    """)

    st_space("v", 1)

    # ── Recipe 2: Citation Review Before Delivery ─────────────────
    st_write(bs.sub, "Citation Review Before Delivery", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             "Your document cites external sources (URLs, papers, books). "
             "Before publishing, you want a targeted review that checks "
             "citation accuracy, link validity, and proper attribution.")
    st_space("v", 0.5)

    show_code("""\
        /stx-ce:task review "Verify all citations: check URLs, author names, dates"
    """, language="bash", line_numbers=False)
    st_space("v", 0.5)

    show_explanation("""\
    **What happens:**
    1. The ad-hoc reviewer scans all blocks for citation patterns
       (URLs, bibliography references, inline attributions)
    2. It checks URL reachability where possible
    3. It cross-references author names and dates with source files
    4. Findings are saved to `docs/reviews/task-review.md`

    **Expected result:** A findings table with severity levels. Dead URLs
    are flagged as CRITICAL, misspelled names as MINOR, missing dates
    as MAJOR. You can then run `/stx-ce:fix` to address the findings.
    """)

    st_space("v", 1)

    # ── Recipe 3: Emergency Block Addition ────────────────────────
    st_write(bs.sub, "Emergency Block Addition", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             "The review revealed a missing topic that should have been "
             "in the plan. You need to add a block without restarting "
             "the entire cycle.")
    st_space("v", 0.5)

    show_code("""\
        /stx-ce:task produce "Add a block about error handling best practices after bck_api_basics"
    """, language="bash", line_numbers=False)
    st_space("v", 0.5)

    show_explanation("""\
    **What happens:**
    1. CE reads the current plan and identifies the insertion point
    2. A new block file is created (e.g., `bck_api_error_handling.py`)
    3. The plan is versioned (NNN+1) with a Change Log entry
    4. The block is registered in `book.py` at the specified position
    5. The gate triggers (always mode) — you review the new block

    **Expected result:** A new block file, an updated plan version,
    and a modified `book.py`. The block follows project style conventions
    and fits the narrative flow of its neighbors.
    """)

    st_space("v", 1)

    # ── Recipe 4: Pattern Extraction ──────────────────────────────
    st_write(bs.sub, "Pattern Extraction", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             "You noticed a visual layout pattern that works well and "
             "want to save it as a reusable solution for future projects.")
    st_space("v", 0.5)

    show_code("""\
        /stx-ce:task capitalize "Document the two-column comparison layout used in bck_ce_plan_versioning"
    """, language="bash", line_numbers=False)
    st_space("v", 0.5)

    show_explanation("""\
    **What happens:**
    1. The learnings researcher checks `docs/solutions/` for duplicates
    2. If NOVEL, CE extracts the pattern from the specified block
    3. A solution package is created with context, code, and usage notes
    4. The package is saved to `docs/solutions/`

    **Expected result:** A `tpl_solution_package` file documenting the
    pattern with a description, a minimal code example, and guidance
    on when to use (and when not to use) the pattern. Future cycles
    can reference this solution during PRODUCE.
    """)

    st_space("v", 1)

    # ── Recipe 5: Plan Evolution ──────────────────────────────────
    st_write(bs.sub, "Plan Evolution", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             "After several sessions, the project scope has shifted. "
             "You need to restructure the plan: reorder sections, drop "
             "a chapter, and add new blocks.")
    st_space("v", 0.5)

    show_code("""\
        /stx-ce:task plan-update "Move security to Part 2, drop deprecated chapter, add 3 new blocks for monitoring"
    """, language="bash", line_numbers=False)
    st_space("v", 0.5)

    show_explanation("""\
    **What happens:**
    1. CE reads the current plan (highest sequence number)
    2. It applies the requested modifications to a new copy
    3. A Change Log is prepended documenting each change
    4. The new version is saved with NNN+1
    5. The gate triggers (always mode) — you review the structural changes

    **Expected result:** A new plan version reflecting the restructured
    document. The old version remains in `docs/plans/` for reference.
    Subsequent `/stx-ce:produce` calls automatically pick up the new plan.
    """)

    st_space("v", 1)

    # ── Recipe 6: Returning After a Break ─────────────────────────
    st_write(bs.sub, "Returning After a Break", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             "You have not worked on the project for a week. Before "
             "resuming, you need to understand what state the cycle is "
             "in and whether anything drifted.")
    st_space("v", 0.5)

    show_code("""\
        /stx-ce:continue
    """, language="bash", line_numbers=False)
    st_space("v", 0.5)

    show_explanation("""\
    **What happens:**
    1. CE inspects all artifacts and block files
    2. It detects drift across 5 categories (source, manual, plan, stale, unresolved)
    3. It presents a briefing (project state, last phase, next phase)
    4. It proposes corrective actions ranked by priority
    5. You approve, modify, or dismiss each proposal

    **Expected result:** A clear picture of where you left off and what
    changed since. After addressing any CRITICAL drift, you can resume
    the cycle exactly where you stopped — or adjust course based on
    the new information.
    """)

    st_space("v", 1)

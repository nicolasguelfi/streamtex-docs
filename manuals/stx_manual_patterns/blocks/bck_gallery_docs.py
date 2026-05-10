"""Gallery — documentation patterns: manual_section, feature_walkthrough,
api_reference_card, composite_block.

# @pattern: manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Docs gallery styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    keyword = s.bold + s.project.colors.primary_violet
    accent = s.bold + s.project.colors.accent_teal


bs = BlockStyles


def build():
    """Compact gallery of the four docs-scope patterns."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Docs Patterns Gallery",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    show_explanation("""\
        Four patterns scoped to **documentation manuals**. The
        manual you are reading right now is itself a dogfooding test
        of three of them: every block of `stx_manual_patterns` is
        annotated with `# @pattern: manual_section`,
        `# @pattern: feature_walkthrough`, or
        `# @pattern: api_reference_card`. See the source!
    """)
    st_space("v", 2)

    # ---- manual_section ----
    st_write(bs.sub, "manual_section — explanation + code + demo triad",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The canonical "feature explanation" pattern. A section
        heading, a sub-heading, then for each sub-topic the triad
        **explanation -> code -> live demo**. The current page (and
        almost every other in this manual) is a manual_section.
    """)
    st_space("v", 1)

    show_code("""\
def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "<Topic>", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # ---- Sub-topic ----
        st_write(bs.sub, "<Sub-topic>", toc_lvl="+1")
        show_explanation("...")
        show_code("...")
        # live demo (same code, executed)
        st_space("v", 2)""")
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "docs/manual_section.md"),
             (bs.accent, " for the full INVARIANTS / PARAMS / INTERDITS."))
    st_space("v", 2)

    # ---- feature_walkthrough ----
    st_write(bs.sub, "feature_walkthrough — numbered tutorial",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Sequential, goal-oriented variant: each sub-section is
        "Step 1: ...", "Step 2: ...". The reader follows along and
        achieves a concrete task by the last step. Used for
        Quick-Starts and "How do I X?" recipes.
    """)
    st_space("v", 1)

    show_code("""\
def build():
    st_write(bs.heading, "Quick Start - First Block & Run",
             tag=t.div, toc_lvl="1")
    st_write(bs.sub, "Step 1: Create a block file", toc_lvl="+1")
    show_explanation("...")
    show_code("# blocks/bck_hello.py\\n...")

    st_write(bs.sub, "Step 2: Register in book.py", toc_lvl="+1")
    ...

    st_write(bs.sub, "Step N: Run it", toc_lvl="+1")
    show_code("stx run")""")
    st_space("v", 1)

    show_details("""\
        In this manual, `bck_authoring.py` is annotated
        `# @pattern: feature_walkthrough` — its 7 steps follow the
        pattern verbatim.
    """)
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "docs/feature_walkthrough.md"),
             (bs.accent, " for the contract."))
    st_space("v", 2)

    # ---- api_reference_card ----
    st_write(bs.sub, "api_reference_card — one symbol per page",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A focused reference block: monospace function signature as
        heading, one-line lead, three core sub-sections
        (**Parameters / Returns / Example**), optional `See also`.
        Used for one-symbol-per-page documentation.
    """)
    st_space("v", 1)

    show_code("""\
class BlockStyles:
    heading = (s.project.titles.section_title
               + s.text.fonts.font_monospace + s.center_txt)
    lead = s.project.titles.body + s.center_txt
    sub = s.project.titles.section_subtitle

def build():
    st_write(bs.heading, "st_grid(cols, gap=None, cell_styles=None)",
             tag=t.div, toc_lvl="1")
    st_write(bs.lead, "Lay out content in a CSS grid container.")
    # Parameters / Returns / Example sub-sections...""")
    st_space("v", 1)

    show_details("""\
        In this manual, `bck_cli_overview.py` is annotated
        `# @pattern: api_reference_card` — its monospace heading,
        sub-commands grid, common flags, and examples follow the
        pattern.
    """)
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "docs/api_reference_card.md"),
             (bs.accent, " for the full grammar."))
    st_space("v", 2)

    # ---- composite_block ----
    st_write(bs.sub, "composite_block — orchestrate atomic sub-blocks",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A glue block whose only job is to `st_include` several
        atomic sub-blocks living in a sibling `_atomic/` folder.
        Used to keep individual files small (~200 lines max) while
        still presenting a unified topic in the TOC.
    """)
    st_space("v", 1)

    show_code("""\
import streamtex as stx
from streamtex import st_include


bck_part_a = stx.load_atomic_block("bck_part_a", __file__)
bck_part_b = stx.load_atomic_block("bck_part_b", __file__)


class BlockStyles:
    pass  # composite has no styles of its own
bs = BlockStyles


def build():
    st_include(bck_part_a)
    st_include(bck_part_b)""")
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "docs/composite_block.md"),
             (bs.accent, " for sibling-folder layout and load rules."))
    st_space("v", 1)

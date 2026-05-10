"""Gallery — documentation patterns: manual_section, feature_walkthrough,
api_reference_card, composite_block.

# @pattern: ptn_manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import (
    show_code, show_explanation, show_details, show_and_run,
)


class BlockStyles:
    """Docs gallery styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    sub_local = s.project.titles.section_subtitle + s.center_txt
    body = s.large
    body_c = s.large + s.center_txt
    keyword = s.bold + s.project.colors.primary_violet
    accent = s.bold + s.project.colors.accent_teal
    mono_heading = (
        s.large
        + s.bold
        + s.text.fonts.font_monospace
        + s.center_txt
        + s.project.colors.primary_violet
    )


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
        annotated with `# @pattern: ptn_manual_section`,
        `# @pattern: ptn_feature_walkthrough`, or
        `# @pattern: ptn_api_reference_card`. See the source!
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
        almost every other in this manual) is a manual_section. Below:
        a tiny self-similar instance.
    """)
    st_space("v", 1)

    def _demo_manual_section():
        with st_block(s.project.containers.result_box):
            st_write(bs.sub_local, "<Sub-topic title>", tag=t.div)
            st_space("v", 0.5)
            show_explanation("""\
                Short paragraph that introduces the feature, in
                neutral prose. 2–4 lines is typical.
            """)
            show_code('st_write(s.center_txt, "Hello, manual_section!")')
            st_space("v", 0.5)
            st_write(s.center_txt, "Hello, manual_section!")

    show_and_run(_demo_manual_section)
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "docs/ptn_manual_section.md"),
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

    def _demo_feature_walkthrough():
        with st_block(s.project.containers.result_box):
            st_write(bs.sub_local, "Quick Start — first block",
                     tag=t.div)
            st_space("v", 0.5)
            for n, label in [
                (1, "Create `blocks/bck_hello.py`"),
                (2, "Add it to the registry in `book.py`"),
                (3, "Run `stx run` and refresh the browser"),
            ]:
                st_write(bs.body,
                         (bs.keyword, f"Step {n}. "),
                         label)

    show_and_run(_demo_feature_walkthrough)
    st_space("v", 1)

    show_details("""\
        In this manual, `bck_authoring.py` is annotated
        `# @pattern: ptn_feature_walkthrough` — its 7 steps follow the
        pattern verbatim.
    """)
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "docs/ptn_feature_walkthrough.md"),
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

    def _demo_api_reference_card():
        with st_block(s.project.containers.result_box):
            st_write(bs.mono_heading,
                     "st_grid(cols, gap=None, cell_styles=None)",
                     tag=t.div)
            st_space("v", 0.5)
            st_write(bs.body_c,
                     "Lay out content in a CSS grid container.")
            st_space("v", 0.5)
            st_write(bs.body, (bs.keyword, "Parameters: "),
                     "cols, gap, cell_styles, ...")
            st_write(bs.body, (bs.keyword, "Returns: "),
                     "GridController context manager.")

    show_and_run(_demo_api_reference_card)
    st_space("v", 1)

    show_details("""\
        In this manual, `bck_cli_overview.py` is annotated
        `# @pattern: ptn_api_reference_card` — its monospace heading,
        sub-commands grid, common flags, and examples follow the
        pattern.
    """)
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "docs/ptn_api_reference_card.md"),
             (bs.accent, " for the full grammar."))
    st_space("v", 2)

    # ---- composite_block ----
    st_write(bs.sub, "composite_block — orchestrate atomic sub-blocks",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A glue block whose only job is to compose several atomic
        sub-blocks living in a sibling `_atomic/` folder. Used to keep
        individual files small (~200 lines max) while still presenting
        a unified topic in the TOC. The render below mimics the result
        of three loaded sub-blocks.
    """)
    st_space("v", 1)

    def _demo_composite_block():
        def _atom_a():
            st_write(bs.body_c, (bs.keyword, "[atom A] "),
                     "fundamentals introduction")

        def _atom_b():
            st_write(bs.body_c, (bs.keyword, "[atom B] "),
                     "deeper-dive section")

        def _atom_c():
            st_write(bs.body_c, (bs.keyword, "[atom C] "),
                     "examples and exercises")

        with st_block(s.project.containers.result_box):
            for atom in (_atom_a, _atom_b, _atom_c):
                atom()
                st_space("v", 0.5)

    show_and_run(_demo_composite_block)
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "docs/ptn_composite_block.md"),
             (bs.accent, " for sibling-folder layout and load rules."))
    st_space("v", 1)

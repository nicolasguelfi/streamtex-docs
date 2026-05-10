"""Demo — stat_hero slide template.

# @pattern: ptn_manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import (
    show_explanation, show_details, show_and_run,
)


class BlockStyles:
    """Demo styles for stat_hero."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    slide_title = (
        s.Large + s.bold + s.project.colors.accent_teal + s.center_txt
    )
    stat = (
        s.Huge + s.bold + s.project.colors.primary_violet + s.center_txt
    )
    body_c = s.large + s.center_txt
    keyword = s.bold + s.project.colors.primary_violet
    highlight = s.bold + s.project.colors.highlight_amber
    source = s.large + s.italic + s.center_txt + s.project.colors.neutral_gray


bs = BlockStyles


def build():
    """Dedicated demo for the stat_hero slide template."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Demo — stat_hero",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    # ---- What it is ----
    st_write(bs.sub, "What it is", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A slide whose visual centerpiece is a single oversized
        number or short phrase — the **hero stat** — supported by a
        brief body explanation and a citation. Used to anchor
        evidence-driven slides where one data point must dominate.

        **When to use** — slides whose purpose is to drive home a
        single quantitative insight. **When NOT to use** — multi-stat
        comparisons (use `comparison_table`), syntheses of several
        findings (use `evidence_insight`), qualitative claims (use
        `callout`).
    """)
    st_space("v", 2)

    # ---- Live render (code shown == code rendered) ----
    st_write(bs.sub, "Live render", toc_lvl="+1")
    st_space("v", 1)

    def _demo():
        with st_block(s.project.containers.tip_callout + s.center_txt):
            st_write(bs.slide_title, "The METR Paradox", tag=t.div)
            st_space("v", 1)
            st_write(bs.stat, "+19%")
            st_space("v", 1)
            st_write(bs.body_c,
                     "Slower, not faster, despite the hype.")
            st_space("v", 0.5)
            st_write(bs.body_c,
                     "Predicted ",
                     (bs.keyword, "24% faster"),
                     ", ",
                     (bs.highlight, "still believed"),
                     " they were 20% faster.")
            st_space("v", 1)
            st_write(bs.source, "— METR (2025), arXiv:2507.09089")

    show_and_run(_demo)
    st_space("v", 1)

    show_details("""\
        **INVARIANTS**: exactly one hero stat per slide, an oversized
        style for the number (e.g. `s.project.titles.stat_hero`), and
        a mandatory citation at the bottom. Variants (b) image + stat
        and (c) stat + tooltip add a 2-column grid or a
        `slide_heading` wrapper but never split the focal point.
    """)
    st_space("v", 1)

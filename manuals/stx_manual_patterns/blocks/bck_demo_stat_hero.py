"""Demo — stat_hero slide template.

# @pattern: manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


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

    # ---- Code skeleton ----
    st_write(bs.sub, "Code skeleton", toc_lvl="+1")
    st_space("v", 1)

    show_code("""\
class BlockStyles:
    heading = s.project.titles.slide_title + s.center_txt
    stat = s.project.titles.stat_hero
    body = s.project.titles.body
    keyword = s.bold + s.project.colors.primary
    source = s.project.citation + s.large + s.center_txt
bs = BlockStyles


def build():
    with st_block(s.project.containers.page_fill_top):
        with st_block(s.center_txt):
            st_write(bs.heading, "<Slide title>",
                     tag=t.div, toc_lvl="1")
            st_space("v", 1)
            st_write(bs.stat, "<HERO STAT>")
            st_space("v", 1)
            st_write(bs.body,
                     "<Body explanation, 1-3 lines.>")
            st_space("v", 1)
            st_write(bs.body,
                     (bs.keyword, "<emphasis>"),
                     " <continuation>")
        st_space("v", 1)
        st_write(bs.source, cite("<bib_key>"))""")
    st_space("v", 2)

    # ---- Live render ----
    st_write(bs.sub, "Live render", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A faithful render of variant (a) — stat-only. The citation
        is a static string here so the demo doesn't need a BibTeX
        backend.
    """)
    st_space("v", 1)

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
    st_space("v", 1)

    show_details("""\
        **INVARIANTS**: exactly one hero stat per slide,
        `s.project.titles.stat_hero` for the number, and a
        mandatory `cite` at the bottom. Variants (b) image+stat and
        (c) stat+tooltip add a 2-column grid or a `slide_heading`
        wrapper but never split the focal point.
    """)
    st_space("v", 1)

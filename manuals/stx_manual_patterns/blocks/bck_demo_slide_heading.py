"""Demo — ptn_slide_heading atom.

# @pattern: ptn_manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import (
    show_explanation, show_details, show_and_run,
)


class BlockStyles:
    """Demo styles for ptn_slide_heading."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    slide_title = (
        s.Large + s.bold + s.project.colors.accent_teal + s.center_txt
    )
    keyword = s.bold + s.project.colors.primary_violet
    cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.center_txt
        + s.container.layouts.vertical_center_layout
    )


bs = BlockStyles


def build():
    """Dedicated demo for the ptn_slide_heading atom."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Demo — ptn_slide_heading",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    # ---- What it is ----
    st_write(bs.sub, "What it is", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A 2-cell heading row at the top of nearly every content slide
        in StreamTeX presentations. A grid split **95% / 5%**: the
        slide title dominates the left, a small marker on the right
        gives the presenter optional context (e.g. a hover tooltip).

        **When to use** — every content slide that has a title and
        may need presenter notes. **When NOT to use** — true title
        slides (use `ptn_title_slide`), slide breaks (no title),
        slides where the title spans an image.
    """)
    st_space("v", 2)

    # ---- Live render (code shown == code rendered) ----
    st_write(bs.sub, "Live render", toc_lvl="+1")
    st_space("v", 1)

    def _demo():
        with st_grid(cols="95% 5%", gap="0px", cell_styles=bs.cell) as g:
            with g.cell():
                st_write(
                    bs.slide_title,
                    "Evidence Synthesis — METR Paradox",
                    tag=t.div,
                )
            with g.cell():
                st_write(s.large + s.center_txt, (bs.keyword, "?"))

    show_and_run(_demo)
    st_space("v", 1)

    show_details("""\
        **INVARIANTS** to remember: 95/5 ratio,
        `s.project.titles.slide_title` for the title, marker on the
        **right** sized so popovers do not overflow the projector edge,
        and `toc_lvl` is mandatory.
    """)
    st_space("v", 1)

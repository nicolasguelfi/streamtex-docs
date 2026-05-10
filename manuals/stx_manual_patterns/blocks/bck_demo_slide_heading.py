"""Demo — slide_heading atom (54 occurrences in the corpus).

# @pattern: manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Demo styles for slide_heading."""
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
    """Dedicated demo for the slide_heading atom."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Demo — slide_heading",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    # ---- What it is ----
    st_write(bs.sub, "What it is", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A 2-cell heading row at the top of nearly every content slide
        in the `ai4se6d` collection. A grid split **95% / 5%**: the
        slide title dominates the left, a small hover-tooltip icon
        on the right gives the presenter optional context.

        **When to use** — every content slide that has a title and
        may need presenter notes. **When NOT to use** — true title
        slides (use `title_slide`), slide breaks (no title),
        slides where the title spans an image.
    """)
    st_space("v", 2)

    # ---- Code skeleton ----
    st_write(bs.sub, "Code skeleton", toc_lvl="+1")
    st_space("v", 1)

    show_code("""\
from streamtex import st_grid, st_write, st_zoom
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from shared_widgets import st_hover_tooltip


class BlockStyles:
    heading = s.project.titles.slide_title + s.center_txt
bs = BlockStyles


def build():
    with st_grid(
        cols="95% 5%",
        gap="0px",
        cell_styles=s.project.containers.grid_cell_centered,
    ) as g:
        with g.cell():
            with st_zoom(90):
                st_write(bs.heading, "<Slide title>",
                         tag=t.div, toc_lvl="+1")
        with g.cell():
            st_hover_tooltip(
                title="<Tooltip title>",
                entries=[
                    ("<Label>", "<Body>"),
                    # 2 to 5 entries usually
                ],
                scale="2vw",
                width="70vw",
                position="left",
            )""")
    st_space("v", 2)

    # ---- Live render ----
    st_write(bs.sub, "Live render", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Below is a faithful render of the 95/5 grid (the tooltip is
        replaced by a placeholder square so the demo renders without
        the `shared_widgets` dependency).
    """)
    st_space("v", 1)

    with st_grid(cols="95% 5%", gap="0px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write(bs.slide_title, "Evidence Synthesis — METR Paradox",
                     tag=t.div)
        with g.cell():
            st_write(s.large + s.center_txt, (bs.keyword, "?"))
    st_space("v", 1)

    show_details("""\
        **INVARIANTS** to remember: 95/5 ratio, `s.project.titles.slide_title`
        for the title, tooltip on the **left** (popovers overflow the
        right edge on projectors), and `toc_lvl` is mandatory.
    """)
    st_space("v", 1)

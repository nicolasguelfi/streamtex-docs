from streamtex import *
from streamtex.styles import Style as ns
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Grid basics styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    cell = (s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.center_txt
            + s.container.layouts.vertical_center_layout)
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Grid Basics", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # Integer cols
        st_write(bs.sub, "st_grid with integer columns", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Pass an integer to cols for equal-width columns.
        """)
        st_space("v", 1)

        show_code("""\
with st_grid(cols=3, cell_styles=bs.cell) as g:
    with g.cell(): st_write(s.large, "Cell A1")
    with g.cell(): st_write(s.large, "Cell B1")
    with g.cell(): st_write(s.large, "Cell C1")""")
        st_space("v", 1)

        with st_grid(cols=3, cell_styles=bs.cell) as g:
            with g.cell(): st_write(s.large, "Cell A1")
            with g.cell(): st_write(s.large, "Cell B1")
            with g.cell(): st_write(s.large, "Cell C1")
            with g.cell(): st_write(s.large, "Cell A2")
            with g.cell(): st_write(s.large, "Cell B2")
            with g.cell(): st_write(s.large, "Cell C2")
        st_space("v", 2)

        # String cols
        st_write(bs.sub, "st_grid with string columns", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Pass a CSS grid-template-columns string for custom widths.
        """)
        st_space("v", 1)

        show_code("""\
with st_grid(cols="1fr 2fr", cell_styles=bs.cell) as g:
    with g.cell(): st_write(s.large, "Narrow (1fr)")
    with g.cell(): st_write(s.large, "Wide (2fr)")""")
        st_space("v", 1)

        with st_grid(cols="1fr 2fr", cell_styles=bs.cell) as g:
            with g.cell(): st_write(s.large, "Narrow (1fr)")
            with g.cell(): st_write(s.large, "Wide (2fr)")
            with g.cell(): st_write(s.large, "Sidebar")
            with g.cell(): st_write(s.large, "Main content area takes more space")
        st_space("v", 2)

        # grid_style
        st_write(bs.sub, "grid_style parameter", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            grid_style applies CSS to the entire grid container.
        """)
        st_space("v", 1)

        table_style = ns("table-layout: fixed; width: 100%; border-collapse: collapse;")
        show_code("""\
table_style = ns("table-layout: fixed; width: 100%; border-collapse: collapse;")
with st_grid(cols=2, grid_style=table_style,
             cell_styles=bs.cell) as g:
    with g.cell(): st_write(s.bold + s.large, "Header A")
    with g.cell(): st_write(s.bold + s.large, "Header B")
    with g.cell(): st_write(s.large, "Data A1")
    with g.cell(): st_write(s.large, "Data B1")""")
        st_space("v", 1)

        with st_grid(cols=2, grid_style=table_style, cell_styles=bs.cell) as g:
            with g.cell(): st_write(s.bold + s.large, "Header A")
            with g.cell(): st_write(s.bold + s.large, "Header B")
            with g.cell(): st_write(s.large, "Data A1")
            with g.cell(): st_write(s.large, "Data B1")
        st_space("v", 2)

        show_details("""\
            Defaults: cols=2, grid_style=none, cell_styles=none.

            Cells auto-wrap to new rows when cols limit is reached.

            Use # row N comments for readability in complex grids.
        """)
        st_space("v", 3)

        # responsive_cols helper
        st_write(bs.sub, "responsive_cols() helper", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The responsive_cols() helper generates a CSS grid-template-columns
            value using auto-fit and minmax for adaptive column layouts.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import responsive_cols

# Returns a CSS string like:
# "grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));"
cols_css = responsive_cols(min_width="250px")""")
        st_space("v", 1)

        show_details("""\
            Use this with grid_style for grids that adapt to screen width.

            Columns automatically wrap when the viewport is too narrow.

            Prefer st_grid(responsive=True) for most cases — it uses responsive_cols() internally.
        """)

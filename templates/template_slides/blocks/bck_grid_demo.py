"""Grid demo slide — responsive layout with styled containers."""
from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    body = s.project.titles.body
    body_accent = s.project.titles.body_accent
    caption = s.project.titles.caption + s.center_txt
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Responsive Grids", tag=t.div, toc_lvl="1")
        st_space(size=3)

        with st_grid(cols="1fr 1fr 1fr", gap="24px"):
            with st_block(s.project.containers.callout):
                st_write(bs.body_accent, "Column 1")
                st_space(size=1)
                st_write(bs.body, "Grids adapt to screen size automatically")

            with st_block(s.project.containers.callout):
                st_write(bs.body_accent, "Column 2")
                st_space(size=1)
                st_write(bs.body, "Use st_grid() with CSS grid templates")

            with st_block(s.project.containers.callout):
                st_write(bs.body_accent, "Column 3")
                st_space(size=1)
                st_write(bs.body, "Compose styles with the + operator")

        st_space(size=3)
        st_write(bs.caption, "st_grid(cols='1fr 1fr 1fr', gap='24px')")

    st_slide_break(marker_label="Responsive Grids")

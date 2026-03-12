"""Features slide — two-column layout with key points."""
from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.subtitle
    body = s.project.titles.body
    body_accent = s.project.titles.body_accent
    caption = s.project.titles.caption
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Key Features", tag=t.div, toc_lvl="1")
        st_space(size=3)

        with st_grid(cols="1fr 1fr", gap="32px"):
            # Left column
            with st_block():
                st_write(bs.sub, "Content")
                st_space(size=2)
                with st_list(l_style=bs.body, li_style=bs.body) as l:
                    with l.item(): st_write(bs.body, "Styled text rendering")
                    with l.item(): st_write(bs.body, "Responsive CSS grids")
                    with l.item(): st_write(bs.body_accent, "Dark theme by default")

            # Right column
            with st_block():
                st_write(bs.sub, "Presentation")
                st_space(size=2)
                with st_list(l_style=bs.body, li_style=bs.body) as l:
                    with l.item(): st_write(bs.body, "Fullscreen 16/9 mode")
                    with l.item(): st_write(bs.body, "Slide counter footer")
                    with l.item(): st_write(bs.body_accent, "Keyboard navigation")

        st_space(size=3)
        st_write(bs.caption, "Extend this template by adding new blocks")

    st_slide_break(marker_label="Key Features")

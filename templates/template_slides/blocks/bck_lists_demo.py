"""Lists demo slide — styled lists with mixed content."""
from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.subtitle
    body = s.project.titles.body
    body_accent = s.project.titles.body_accent
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Styled Lists", tag=t.div, toc_lvl="1")
        st_space(size=3)

        with st_grid(cols="1fr 1fr", gap="32px"):
            with st_block():
                st_write(bs.sub, "How to extend")
                st_space(size=2)
                with st_list(style=bs.body) as l:
                    with l.item(): st_write(bs.body, "Add bck_topic.py in blocks/")
                    with l.item(): st_write(bs.body, "Register in book.py list")
                    with l.item(): st_write(bs.body_accent, "Run and iterate")

            with st_block():
                st_write(bs.sub, "Style system")
                st_space(size=2)
                with st_list(style=bs.body) as l:
                    with l.item(): st_write(bs.body, "Edit custom/styles.py")
                    with l.item(): st_write(bs.body, "Compose with + operator")
                    with l.item(): st_write(bs.body_accent, "Theme via custom/themes.py")

    st_slide_break(marker_label="Styled Lists")

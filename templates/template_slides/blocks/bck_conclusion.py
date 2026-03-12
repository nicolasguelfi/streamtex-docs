"""Conclusion slide — summary and next steps."""
from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s


class BlockStyles:
    heading = s.project.titles.slide_title + s.center_txt
    body = s.project.titles.body + s.center_txt
    body_accent = s.project.titles.body_accent + s.center_txt
    caption = s.project.titles.caption + s.center_txt
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_space("v", 3)
        st_write(bs.heading, "Thank You", tag=t.div, toc_lvl="1")
        st_space("v", 3)
        st_write(bs.body, "Add your own slides:")
        st_space("v", 2)
        with st_list(style=bs.body + s.center_txt) as l:
            with l.item(): st_write(bs.body, "Create blocks/bck_topic.py")
            with l.item(): st_write(bs.body, "Add to the list in book.py")
            with l.item(): st_write(bs.body_accent, "Use /stx-designer:update to add content with AI")
        st_space("v", 3)
        st_write(bs.caption, "Built with StreamTeX")
        st_space("v", 3)
